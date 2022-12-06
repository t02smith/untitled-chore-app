from fastapi import APIRouter, Depends
from lib.db.user import User
from lib.auth.user import get_current_active_user
from lib.db import chores
from routes.username import house

router = APIRouter(prefix="/{username}")
router.include_router(house.router)
