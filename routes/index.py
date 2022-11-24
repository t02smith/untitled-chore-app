from fastapi import APIRouter, Depends
from routes.chores import index as chores
from routes.house import index as house
from routes.users import index as users
from lib.auth.user import get_current_user, User


router = APIRouter(prefix="/api/v1")
router.include_router(chores.router)
router.include_router(house.router)
router.include_router(users.router)