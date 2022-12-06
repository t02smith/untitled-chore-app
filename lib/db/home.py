from lib.db import user, db
from typing import List
from pydantic import BaseModel
from fastapi import HTTPException

class Home(BaseModel):
  id: str
  name: str
  residents: List[str]
  chores: List[str]
  creator: str
  
class HomeIn(BaseModel):
  name: str
  residents: List[str] | None = None
  chores: List[str] | None = None
  
class HomeUpdate(BaseModel):
  name: str | None = None
  

async def create_home(home: HomeIn, user: user.User):
  async with db.get_client() as client:
    container_homes = await db.get_or_create_container(client, "homes")
    container_users = await db.get_or_create_container(client, "users")
    
    users_res = container_users.query_items(
      """
      SELECT u.username
      FROM users u
      WHERE ARRAY_CONTAINS(@username, u.username)
      """,
      parameters=[{"name": "@username", "value": home.residents}],
    )
    
    res = [u["username"] async for u in users_res]
      
    res.append(user.username)
    res = await container_homes.create_item(
      {
        "name": home.name,
        "residents": res,
        "chores": [] if home.chores is None else home.chores,
        "creator": user.username
      },
      enable_automatic_id_generation=True,
    )
    
    return Home(**res)
  
async def update_home(homeUpdate: HomeUpdate, creator: str, house_name: str, user: user.User):
  async with db.get_client() as client:
    container_homes = await db.get_or_create_container(client, "homes")
    
    # home_res = await container_homes.read_item(id, partition_key=id)
    home_res = container_homes.query_items(
      """
      SELECT * 
      FROM homes h
      WHERE h.creator=@creator AND h.name=@name
      """, parameters=[{"name": "@creator", "value": creator}, {"name": "@name", "value": house_name}]
    )
    
    homes = [Home(**h) async for h in home_res]
    if len(homes) == 0:
      raise HTTPException(404)
    
    home = homes[0]
    home.name = home.name if homeUpdate.name == None else homeUpdate.name
    return Home(**await container_homes.upsert_item(home.__dict__))


async def get_homes(user: user.User):
  async with db.get_client() as client:
    container = await db.get_or_create_container(client, "homes")

    res = container.query_items(
      """
      SELECT h.name
      from homes h
      WHERE ARRAY_CONTAINS (h['residents'], @username)
      """,
      parameters=[{"name": "@username", "value": user.username}])  

    res2 = [r["name"] async for r in res]
    return res2
  
async def get_home(id: str):
  async with db.get_client() as client:
    container = await db.get_or_create_container(client, "homes")

    res = await container.read_item(id, partition_key=id)
    
    return Home(**res)

async def delete_home(id: str, user: user.User):
  async with db.get_client() as client:
    container = await db.get_or_create_container(client, "homes")

    res = await container.read_item(id, partition_key=id)
    
    if (res["creator"] == user.username):
      await container.delete_item(id, partition_key=id)
    else:
      raise HTTPException(401, "Not the creator")