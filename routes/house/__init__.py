from fastapi import APIRouter, Depends
from lib.db import home
from lib.auth.user import get_current_active_user, User

router = APIRouter(prefix="/house")

@router.post("/")
async def create_home(
  newhome: home.HomeIn, user: User = Depends(get_current_active_user)
):
  return await home.register_home(newhome, user.username)