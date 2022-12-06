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
  

async def register_home(home: HomeIn, user: user.User):
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
  
async def update_home(home: HomeUpdate, id: str, user: user.User):
  async with db.get_client() as client:
    container_homes = await db.get_or_create_container(client, "homes")
    
    home_res = await container_homes.read_item(id, partition_key=id)
    
    if (home_res["creator"] == user.username):
      home_res["name"] = home.name if home.name != None else home_res["name"]
      await container_homes.upsert_item(home_res)
      return Home(**home_res)
    else:
      raise HTTPException(401, "Not the creator")

async def get_homes(user: user.User):
  async with db.get_client() as client:
    container = await db.get_or_create_container(client, "homes")

    res = container.query_items(
      """
      SELECT c.name
      from c
      WHERE ARRAY_CONTAINS (c['residents'], @username)
      """,
      parameters=[{"name": "@username", "value": user.username}])  

    return [Home(**r) async for r in res]
  
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