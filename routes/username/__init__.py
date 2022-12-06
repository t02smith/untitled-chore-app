from fastapi import APIRouter, Depends, HTTPException
from lib.auth.user import get_current_active_user
from lib.db import chores, user as userDB
from typing import List
from routes.username import house

router = APIRouter(prefix="/{username}")

router.include_router(house.router)


@router.get("/")
async def get_user_info(
    username: str, user: userDB.User = Depends(get_current_active_user)
):
    return userDB.UserOut(**user.__dict__)


@router.put("/")
async def update_user_info(
    username: str,
    updated: userDB.UserUpdate,
    user: userDB.User = Depends(get_current_active_user),
):
    if username != user.username:
        raise HTTPException(403)
    return await userDB.update_user(user, updated)


@router.get(
    "/chores",
    description="Get a list of chores created by a user",
    tags=["chores", "user"],
    response_model=List[chores.Chore],
)
async def get_user_chores(
    username: str, user: userDB.User = Depends(get_current_active_user)
):
    return await chores.get_chores_from_user(username, user.username == username)


@router.get(
    "/timetable",
    description="Returns the user's timetable that includes every household.",
)
async def get_user_timetable(
    username, user: userDB.User = Depends(get_current_active_user)
):
    return "timetable"
