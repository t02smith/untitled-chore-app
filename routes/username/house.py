from fastapi import APIRouter, Depends, HTTPException
from lib.db import  user as userDB, home
from lib.auth import user as userAuth

router = APIRouter(prefix="/{house_name}")

@router.put(
  "/",
  description="Update an existing house",
  tags=["house"]
)
async def update_home(
  username: str, house_name: str, newHome: home.HomeIn, user: userDB.User = Depends(userAuth.get_current_active_user)
):
  if username != user.username:
    raise HTTPException(403)
  
  return await home.update_home(newHome, username, house_name, user)