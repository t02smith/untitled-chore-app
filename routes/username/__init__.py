from fastapi import APIRouter, Depends
from lib.db.user import User
from lib.auth.user import get_current_active_user

router = APIRouter(prefix="/{username}")


@router.get("/")
async def chores(
    username: str, user: User = Depends(get_current_active_user), amount: int = 5
):
    # ? are the given username and authenticated user the same
    if username != user.username:
        raise HTTPException(
            status_code=403,
            detail="You cannot access another user's chores",
        )

    # ? does the user exist

    # ? get chores

    return username
