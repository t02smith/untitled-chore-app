from fastapi import APIRouter, Depends
from lib.db import home, types
from lib.auth.user import get_current_active_user
from typing import List
from lib import err

router = APIRouter(prefix="/homes")

@router.post(
  "",
  description="Create a new house where the creator is a resident",
  tags=["home"],
  status_code=201,
  response_model=types.Home,
  responses={
    400: {"description": "User already has the max number of homes or already has a home with that name", "model": err.HTTPError}
  }
)
async def create_home(newHome: types.HomeIn, user: types.User = Depends(get_current_active_user)):
  return await home.create_home(newHome, user)

@router.get(
  "/",
  tags=["home"],
  description="Get a list of a user's homes",
  response_model=List[types.Home],
  status_code=200
)
async def get_homes(user: types.User = Depends(get_current_active_user)): 
  return await home.get_users_homes(user)