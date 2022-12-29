from fastapi import APIRouter, Depends
from lib.db import chores, types
from lib.auth.user import get_current_active_user
from typing import List

router = APIRouter(prefix="/chores")


@router.post(
    "/",
    description="Creates a new chore by a specific user",
    name="Create Chore",
    response_model=types.Chore,
    tags=["chores"],
)
async def create_chore(
    chore: types.ChoreIn, user: types.User = Depends(get_current_active_user)
):
    return await chores.create_chore(chore, user)


@router.get(
    "/",
    description="Get a list of the current user's chores",
    name="Get User Chores",
    response_model=List[types.Chore],
    tags=["chores"],
)
async def get_chores(user: types.User = Depends(get_current_active_user)):
    return await chores.get_chores_from_user(user.username)


@router.get(
    "/",
    description="Get a chore by its ID",
    name="Get a Chore by ID",
    response_model=types.Chore,
    tags=["chores"],
)
async def get_chore_by_id(id: str, user: types.User = Depends(get_current_active_user)):
    return await chores.get_chore_by_id(id, user.username)


@router.put(
    "/",
    description="Update the fields of an existing chore",
    response_model=types.Chore,
    tags=["chores"],
)
async def update_chore(
    id: str, chore: types.ChoreIn, user: types.User = Depends(get_current_active_user)
):
    return await chores.update_chore(id, chore, user.username)

@router.get(
  "/default",
  description="Get a default set of chores",
  response_model=List[types.Chore],
  tags=["chores"]
)
async def get_default_chores():
  return await chores.default_chores()