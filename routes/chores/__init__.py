from fastapi import APIRouter, Depends
from lib.db import chores
from lib.db.user import User
from lib.auth.user import get_current_active_user
from typing import List

router = APIRouter(prefix="/chores")


@router.post(
    "/",
    description="Creates a new chore by a specific user",
    name="Create Chore",
    response_model=chores.Chore,
    tags=["chores"],
)
async def create_chore(
    chore: chores.ChoreIn, user: User = Depends(get_current_active_user)
):
    return await chores.create_chore(chore, user)


@router.get(
    "/",
    description="Get a list of the current user's chores",
    name="Get User Chores",
    response_model=List[chores.Chore],
    tags=["chores"],
)
async def get_chores(user: User = Depends(get_current_active_user)):
    return await chores.get_chores_from_user(user.username)


@router.get(
    "/",
    description="Get a chore by its ID",
    name="Get a Chore by ID",
    response_model=chores.Chore,
    tags=["chores"],
)
async def get_chore_by_id(id: str, user: User = Depends(get_current_active_user)):
    return await chores.get_chore_by_id(id, user.username)


@router.put(
    "/",
    description="Update the fields of an existing chore",
    response_model=chores.Chore,
    tags=["chores"],
)
async def update_chore(
    id: str, chore: chores.ChoreIn, user: User = Depends(get_current_active_user)
):
    return await chores.update_chore(id, chore, user.username)
