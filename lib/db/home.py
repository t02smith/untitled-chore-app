from lib.db import user, db
from typing import List
from pydantic import BaseModel

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
  

async def register_home(home: HomeIn, creator: str):
  async with db.get_client() as client:
    containerHomes = await db.get_or_create_container(client, "homes")
    containerUsers = await db.get_or_create_container(client, "users")
    
    users_res = containerUsers.query_items(
      """
      SELECT u.username
      FROM users u
      WHERE ARRAY_CONTAINS(@username, u.username)
      """,
      parameters=[{"name": "@username", "value": home.residents}],
    )
    
    res = [u["username"] async for u in users_res]
      
    res.append(creator)
    res = await containerHomes.create_item(
      {
        "name": home.name,
        "residents": res,
        "chores": [] if home.chores is None else home.chores,
        "creator": creator
      },
      enable_automatic_id_generation=True,
    )
    
    return Home(**res)
  
async def update_home(home: HomeUpdate):
  return
  