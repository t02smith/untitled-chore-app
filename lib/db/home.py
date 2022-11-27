from lib.db import user, db
from typing import List
from pydantic import BaseModel

class Home:
  id: str
  name: str
  residents: List[str]
  chores: List[str]
  creator: str
  
class HomeIn(BaseModel):
  name: str
  residents: List[str] | None = None
  chores: List[str] | None = None

async def register_home(home: HomeIn, creator: str):
  async with db.get_client() as client:
    container = await db.get_or_create_container(client, "homes")
    
    if home.residents is None:
      home.residents = []
      
    home.residents.append(creator)
    await container.create_item(
      {
        "name": home.name,
        "residents": home.residents,
        "chores": [] if home.chores is None else home.chores,
        "creator": creator
      },
      enable_automatic_id_generation=True,
    )