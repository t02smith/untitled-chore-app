from fastapi import APIRouter, Depends, HTTPException
from lib.auth.user import get_current_active_user
from lib.db import chores, user as userDB, types, timetable
from lib import err, io
from typing import List
from routes.username import house

router = APIRouter(prefix="/{username}")
router.include_router(house.router)

@router.get(
    "/",
    description="Gets information about a user",
    tags=["user"],
    response_model=types.UserOut,
    status_code=200,
    responses={404: {"message": "user not found", "model": err.HTTPError}},
)
async def get_user_info(
    username: str, user: types.User = Depends(get_current_active_user)
):
    if user.username != username:
        userLookup = await userDB.get_user_by_username(username)
        if userLookup is None:
            raise HTTPException(404)

        return types.UserOut(
            username=userLookup.username, first_name=userLookup.first_name
        )

    return userDB.UserOut(**user.__dict__)


@router.put(
    "/",
    description="Update a user's information",
    tags=["user"],
    response_model=types.UserOut,
    status_code=200,
    responses={
        403: {"message": "User not authorized to change this user's details","model": err.HTTPError,}
    },
)
async def update_user_info(
    username: str,
    updated: types.UserUpdate,
    user: types.User = Depends(get_current_active_user),
):
    if username != user.username:
        raise HTTPException(403)

    return await userDB.update_user(user, updated)


@router.get(
    "/chores",
    description="Get a list of chores created by a user",
    tags=["chores", "user"],
    response_model=List[types.Chore],
    status_code=200,
    responses={404: {"message": "User not found", "model": err.HTTPError}},
)
async def get_user_chores(
    username: str, user: types.User = Depends(get_current_active_user)
):
    if await userDB.get_user_by_username(username) is None:
        raise HTTPException(404)

    return await chores.get_chores_from_user(username, user.username == username)


@router.get(
    "/timetable",
    tags=["timetable"],
    description="Returns the user's timetable that includes every household.",
    status_code=200,
    responses={
      403: {"message": "A user tries to access someone else's timetable", "model": err.HTTPError}
    }
)
async def get_user_timetable(
    username, user: types.User = Depends(get_current_active_user)
):
    if username != user.username:
      raise HTTPException(403)
      
    return await timetable.get_users_timetable(user)


@router.post(
  "/timetable/upload", 
  description="Upload your university timetable",
  tags=["timetable"]
)
async def upload_timetable(
    url: str, user: types.User = Depends(get_current_active_user)
):
    if not re.search("https:\/\/timetable\.soton\.ac\.uk\/Feed\/Index\/.*", url):
        raise HTTPException(400, detail="Invalid URL")

    io.read_calendar(url)
    return "OK"
