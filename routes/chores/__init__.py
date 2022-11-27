from fastapi import APIRouter, Depends
from lib.db import chores
from lib.auth.user import get_current_active_user, User

router = APIRouter(prefix="/chores")


@router.post("/")
async def create_chore(
    chore: chores.ChoreIn, user: User = Depends(get_current_active_user)
):
    return await chores.create_chore(chore, user)
