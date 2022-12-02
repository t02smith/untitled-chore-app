from fastapi import APIRouter, Depends, HTTPException
from lib.auth.user import get_current_active_user
from lib.db import chores, user as userDB
from lib.io import read_calendar
import re

router = APIRouter(prefix="/timetable")


@router.post("/uploadUniversityTimetable")
async def upload_timetable(url: str):
    # TODO check that the URL goes to timetable.soton
    if not re.search("https:\/\/timetable\.soton\.ac\.uk\/Feed\/Index\/.*", url):
        raise HTTPException(400)

    read_calendar(url)
    return "OK"
