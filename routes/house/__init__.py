from fastapi import APIRouter, Depends
from lib.db import home, types
from lib.auth.user import get_current_active_user

router = APIRouter(prefix="/house")


@router.post(
    "/",
    description="Create a new house where the creator is a resident.",
    tags=["house"],
)
async def create_home(
    newhome: types.HomeIn, user: types.User = Depends(get_current_active_user)
):
    return await home.create_home(newhome, user.username)


@router.get(
    "/getHomes", description="Get the homes that contain a certain user", tags=["house"]
)
async def get_homes(user: types.User = Depends(get_current_active_user)):
    return await home.get_homes(user)


@router.get("/getHome", description="Get a home by id", tags=["house"])
async def get_home(id: str, user: types.User = Depends(get_current_active_user)):
    return await home.get_homes(id)


@router.delete(
    "/deleteHome",
    description="Delete a house by id. Only the creator of the house can do this",
    tags=["house"],
)
async def delete_home(id: str, user: types.User = Depends(get_current_active_user)):
    return await home.delete_home(id, user)
