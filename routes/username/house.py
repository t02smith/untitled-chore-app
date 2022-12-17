from fastapi import APIRouter, Depends, HTTPException
from lib.db import user as userDB, home, chores, timetable, types
from lib.auth import user as userAuth
from lib import err
from typing import List

router = APIRouter(prefix="/{house_name}")


@router.get("/", tags=["house"])
async def get_home(username: str, house_name: str, user: types.User = Depends(userAuth.get_current_active_user)):
    return await home.get_home_by_creator_and_name(username, house_name, user)


@router.get("/timetable")
async def get_home_timetable():
    pass


@router.put("/", description="Update an existing house", tags=["home"])
async def update_home(
    username: str,
    house_name: str,
    newHome: types.HomeIn,
    user: types.User = Depends(userAuth.get_current_active_user),
):
    if username != user.username:
        raise HTTPException(403)

    return await home.update_home(newHome, username, house_name, user)


# ! CHORES


@router.get(
    "/chores",
    description="Get a list of chores by house",
    summary="Get a list of chores by house",
    tags=["home"],
    response_model=List[types.Chore],
    status_code=200,
    responses={
        404: {"message": "house not found", "model": err.HTTPError},
        403: {"message": "user not in house", "model": err.HTTPError},
    },
)
async def get_house_chores(
    username: str,
    house_name: str,
    user: types.User = Depends(userAuth.get_current_active_user),
):
    house = await home.get_home_by_creator_and_name(username, house_name)
    if house is None:
        raise HTTPException(404)

    if user.username not in house.residents:
        raise HTTPException(403)

    return house.chores


# ! INVITES


@router.post(
    "/invite",
    description="Creates a temporary invite link for your home",
    status_code=201,
    tags=["user", "home"],
    response_model=types.HomeInvite,
    responses={
        403: {"message": "Not authorized to make a link", "model": err.HTTPError},
        404: {"message": "Home not found", "model": err.HTTPError},
    },
)
async def create_invite_link(
    username: str,
    house_name: str,
    user: types.User = Depends(userAuth.get_current_active_user),
):
    if username != user.username:
        raise HTTPException(403)

    return await home.create_invite_link(username, house_name, user)


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
    user: types.User = Depends(userAuth.get_current_active_user),
):
    await home.join_home_via_invite_link(username, house_name, invite_id, user)
    return "Joined home successfully"


# ! TIMETABLE


@router.get(
    "/timetable",
    summary="Get this week's timetable for a given house",
    status_code=200,
    tags=["home"],
)
async def get_or_generate_timetable(
    username: str,
    house_name: str,
    user: types.User = Depends(userAuth.get_current_active_user),
):
    # return await timetable.get_or_generate_timetable(
    #     username, house_name, user.username
    # )
    pass
