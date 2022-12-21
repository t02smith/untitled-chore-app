from fastapi import APIRouter, Depends, HTTPException
from lib.db import user as userDB, home, chores, timetable, types
from lib.auth import user as userAuth
from lib import err
from typing import List

router = APIRouter(prefix="/{house_name}")


@router.get(
  "/", 
  tags=["home"], 
  status_code=200, 
  response_model=types.Home, 
  description="Returns a JSON object of a home if the user has sufficient permissions to view it.",
  responses={
    403: {"description": "User doesn't have permission to view this house", "model": err.HTTPError},
    404: {"description": "House not found", "model": err.HTTPError}
  }
)
async def get_home(username: str, house_name: str, user: types.User = Depends(userAuth.get_current_active_user)):
    return await home.get_home_by_creator_and_name(username, house_name, user)


@router.put("/", description="Update an existing house", tags=["home"])
async def update_home(
    username: str,
    house_name: str,
    newHome: types.HomeIn,
    user: types.User = Depends(userAuth.get_current_active_user),
):
    if username != user.username:
        raise HTTPException(403, detail="You do not have permission to update this home")

    return await home.update_home(newHome, username, house_name, user)


@router.put(
  "/timetable", 
  tags=["home"],
  description="Get this week's chore timetable or generate one if it doesn't exist or is expired",
  status_code=200,
  response_model=types.Timetable,
  responses={
    403: {"description": "You do not have permission to view this timetable", "model": err.HTTPError},
    404: {"description": "House not found", "model": err.HTTPError}
  }  
)
async def get_home_timetable(username: str, house_name: str, user: types.User = Depends(userAuth.get_current_active_user) ):
    res = await timetable.get_or_generate_timetable(username, house_name, user)
    if res is None:
      raise HTTPException(500)
    
    return res


@router.put(
  "/complete", 
  description="Set a user's task to complete",
  tags=["home", "timetable"],
  status_code=200,
  response_model=types.TimetabledChore,
  responses={
    302: {"description": "The timetable needs to be regenerated before this can be called"},
    400: {"description": "The chore is already complete or the timetable is expired", "model": err.HTTPError},
    403: {"description": "The chore isn't assigned to the user trying to complete or the user is not in the house", "model": err.HTTPError},
    404: {"description": "The house doesn't exist or the chore isn't part of the timetable", "model": err.HTTPError}
  }
)
async def complete_task(username: str, house_name: str, chore_id: str, user: types.User = Depends(userAuth.get_current_active_user)):
  return await timetable.complete_task(username, house_name, chore_id, user)


# ! CHORES


@router.get(
    "/chores",
    description="Get a list of chores by house",
    summary="Get a list of chores by house",
    tags=["home"],
    response_model=List[types.Chore],
    status_code=200,
    responses={
        404: {"description": "house not found", "model": err.HTTPError},
        403: {"description": "user not in house", "model": err.HTTPError},
    },
)
async def get_house_chores(
    username: str,
    house_name: str,
    user: types.User = Depends(userAuth.get_current_active_user),
):
    return (await home.get_home_by_creator_and_name(username, house_name)).chores


# ! INVITES


@router.post(
    "/invite",
    description="Creates a temporary invite link for your home",
    status_code=201,
    tags=["user", "home"],
    response_model=types.HomeInvite,
    responses={
        403: {"description": "Not authorized to make a link", "model": err.HTTPError},
        404: {"description": "Home not found", "model": err.HTTPError},
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
            "description": "Invalid invite link or user already in home",
            "model": err.HTTPError,
        },
        404: {"description": "Home not found", "model": err.HTTPError},
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
