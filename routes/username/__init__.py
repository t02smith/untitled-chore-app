from fastapi import APIRouter, Depends
from lib.auth.user import get_current_active_user
from lib.db import chores, user
from typing import List

router = APIRouter(prefix="/{username}")


@router.get(
    "/chores",
    description="Get a list of chores created by a user",
    tags=["chores", "user"],
    response_model=List[chores.Chore],
)
async def get_user_chores(
    username: str, user: user.User = Depends(get_current_active_user)
):
    return await chores.get_chores_from_user(username, user.username == username)
