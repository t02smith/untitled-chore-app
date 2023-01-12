from fastapi import APIRouter, Depends, HTTPException
from lib.auth.user import get_current_active_user
from lib.db import chores, user as userDB, types, timetable, home
from lib import err, io
from typing import List
from routes.username import house

router = APIRouter(prefix="/{username}")
router.include_router(house.router)

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


