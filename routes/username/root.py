from fastapi import APIRouter, Depends, HTTPException
from lib.auth.user import get_current_active_user
from lib.db import chores, user as userDB, types, timetable, home
from lib import err, io
from typing import List
from routes.username import house

router = APIRouter(prefix="/{username}")
router.include_router(house.router)


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


# @router.post(
#   "/timetable/upload", 
#   description="Upload your university timetable",
#   tags=["timetable"]
# )
# async def upload_timetable(
#     url: str, user: types.User = Depends(get_current_active_user)
# ):
#     if not re.search("https:\/\/timetable\.soton\.ac\.uk\/Feed\/Index\/.*", url):
#         raise HTTPException(400, detail="Invalid URL")

#     io.read_calendar(url)
#     return "OK"


