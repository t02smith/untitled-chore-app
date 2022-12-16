from fastapi import APIRouter, Depends, HTTPException
from lib.auth.user import get_current_active_user
from lib.db import chores, user as userDB
from lib import err, io
from typing import List
from routes.username import house

router = APIRouter(prefix="/{username}")

router.include_router(house.router)


@router.get(
    "/",
    description="Gets information about a user",
    tags=["user"],
    response_model=userDB.UserOut | userDB.UserOutPublic,
    status_code=200,
    responses={404: {"message": "user not found", "model": err.HTTPError}},
)
async def get_user_info(
    username: str, user: userDB.User = Depends(get_current_active_user)
):
    if user.username != username:
        userLookup = await userDB.get_user_by_username(username)
        if userLookup is None:
            raise HTTPException(404)

        return userDB.UserOutPublic(**userLookup.__dict__)

    return userDB.UserOut(**user.__dict__)


@router.put(
    "/",
    description="Update a user's information",
    tags=["user"],
    response_model=userDB.UserOut,
    status_code=200,
    responses={
        403: {
            "message": "User not authorized to change this user's details",
            "model": err.HTTPError,
        }
    },
)
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
    status_code=200,
    responses={404: {"message": "User not found", "model": err.HTTPError}},
)
async def get_user_chores(
    username: str, user: userDB.User = Depends(get_current_active_user)
):
    if await userDB.get_user_by_username(username) is None:
        raise HTTPException(404)

    return await chores.get_chores_from_user(username, user.username == username)


@router.get(
    "/timetable",
    description="Returns the user's timetable that includes every household.",
)
async def get_user_timetable(
    username, user: userDB.User = Depends(get_current_active_user)
):
    return "timetable"


@router.post("/timetable/upload", description="Upload your university timetable")
async def upload_timetable(
    url: str, user: userDB.User = Depends(get_current_active_user)
):
    if not re.search("https:\/\/timetable\.soton\.ac\.uk\/Feed\/Index\/.*", url):
        raise HTTPException(400, detail="Invalid URL")

    io.read_calendar(url)
    return "OK"
