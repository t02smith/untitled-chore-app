from fastapi import APIRouter, Depends, HTTPException
from lib.auth.user import get_current_active_user
from lib.db import chores, user as userDB
from lib.io import read_calendar
import re
from lib import err

router = APIRouter(prefix="/timetable")


@router.post(
    "/uploadUniversityTimetable",
    description="Upload your university timetable to untitled-chore-api. This can be found at https://timetable.soton.ac.uk/Feed/Get",
    tags=["user"],
    status_code=200,
    responses={400: {"message": ""}},
)
async def upload_timetable(url: str):
    # TODO check that the URL goes to timetable.soton
    if not re.search("https:\/\/timetable\.soton\.ac\.uk\/Feed\/Index\/.*", url):
        raise HTTPException(400, detail="Invalid URL")

    read_calendar(url)
    return "OK"
