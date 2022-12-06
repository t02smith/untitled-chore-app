from fastapi import APIRouter, Depends, HTTPException
from lib.db import user as userDB, home
from lib.auth import user as userAuth
from lib import err

router = APIRouter(prefix="/{house_name}")


@router.put("/", description="Update an existing house", tags=["house"])
async def update_home(
    username: str,
    house_name: str,
    newHome: home.HomeIn,
    user: userDB.User = Depends(userAuth.get_current_active_user),
):
    if username != user.username:
        raise HTTPException(403)

    return await home.update_home(newHome, username, house_name, user)


@router.get("/")
async def get_home(username: str, house_name: str):
    pass


@router.get("/timetable")
async def get_home_timetable():
    pass


@router.post(
    "/invite",
    description="Creates a temporary invite link for your home",
    status_code=201,
    tags=["user", "home"],
    responses={
        403: {"message": "Not authorized to make a link", "model": err.HTTPError},
        404: {"message": "Home not found", "model": err.HTTPError},
    },
)
async def create_invite_link(
    username: str,
    house_name: str,
    user: userDB.User = Depends(userAuth.get_current_active_user),
):
    if username != user.username:
        raise HTTPException(403)

    return f"{await home.create_invite_link(username, house_name, user)}"


@router.get(
    "/join",
    description="Join a home via an invite link",
    status_code=200,
    tags=["user", "home"],
    responses={
        400: {
            "message": "Invalid invite link or user already in home",
            "model": err.HTTPError,
        },
        404: {"message": "Home not found", "model": err.HTTPError},
    },
)
async def join_home_via_invite_link(
    username: str,
    house_name: str,
    invite_id: str,
    user: userDB.User = Depends(userAuth.get_current_active_user),
):
    await home.join_home_via_invite_link(invite_id, user)
    return "Joined home successfully"
