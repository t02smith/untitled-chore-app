from fastapi import APIRouter, Depends
from lib.db import home
from lib.auth.user import get_current_active_user
from lib.db.user import User

router = APIRouter(prefix="/house")


@router.post(
  "/",
  description="Create a new home",
  response_model=home.Home,
  tags="house"
)
async def create_home(
    newhome: home.HomeIn, user: User = Depends(get_current_active_user)
):
  return await home.create_home(newhome, user.username)

@router.put(
  "/",
  description="Update an existing house",
  response_model=home.Home,
  tags="house"
)
async def update_home(
  id: str, newHome: home.HomeIn, user: User = Depends(get_current_active_user)
):
  return await home.update_home(newHome, id, user)

@router.get(
  "/",
  description="Get the homes that contain a certain user",
  response_model=[home.Home],
  tags="house"
)
async def get_homes(user: User = Depends(get_current_active_user)):
  return await home.get_homes(user)

@router.get(
  "/",
  description="Get a home by id",
  response_model=home.Home,
  tags="house"
)
async def get_home(id: str, user: User = Depends(get_current_active_user)):
  return await home.get_homes(id)

@router.delete(
  "/",
  description="Delete a house by id. Only the creator of the house can do this",
  response_model=home.Home,
  tags="house"
)
async def delete_home(id: str, user: User = Depends(get_current_active_user)):
  return await home.delete_home(id, user)