from fastapi import APIRouter, Depends
from lib.db import home, types
from lib.auth.user import get_current_active_user
from typing import List

router = APIRouter(prefix="/homes")

@router.post(
  "",
  description="Create a new house where the creator is a resident",
  tags=["home"],
  status_code=201,
  response_model=types.Home
)
async def create_home(newHome: types.HomeIn, user: types.User = Depends(get_current_active_user)):
  return await home.create_home(newHome, user)