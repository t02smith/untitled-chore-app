from fastapi import APIRouter, Depends
from lib.db import home
from lib.auth.user import get_current_active_user, User

router = APIRouter(prefix="/house")


@router.post(
    "/",
    description="Create a new house where the creator is a resident.",
    tags=["house"],
)
async def create_home(
    newhome: home.HomeIn, user: User = Depends(get_current_active_user)
):
    await home.register_home(newhome, user.username)


@router.get(
    "/timetable",
    description="Get the current weeks timetable for this household.",
    tags=["timetable", "house"],
)
async def get_timetable(home_id: str, user: User = Depends(get_current_active_user)):
    return ""


@router.post(
    "/timetable",
    description="Generate a new timetable for this week.",
    tags=["timetable", "house"],
)
async def new_timetable(home_id: str, user: User = Depends(get_current_active_user)):
    return ""
