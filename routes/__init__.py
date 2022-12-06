from fastapi import APIRouter, Depends, HTTPException
from routes import chores, house, username, timetable
from lib.auth.user import get_current_active_user
from lib.db.db import get_or_create_database
from lib.db.user import UserIn, User, register_user
from lib.auth import tokens, user as userAuth, auth
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta


router = APIRouter(prefix="/api/v1")
router.include_router(chores.router)
router.include_router(house.router)
router.include_router(username.router)
router.include_router(timetable.router)


@router.post(
    "/login",
    response_model=tokens.Token,
    description="Login using an existing account to untitled-chore-api",
    status_code=201,
    responses={
        401: {"message": "Incorrect username or password"},
        400: {"message": "Invalid username or password"},
    },
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not User.username_valid(form_data.username):
        raise HTTPException(
            400,
            detail="Invalid username or password",
        )

    user = await userAuth.authenticate_user(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_Expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = tokens.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_Expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/register",
    response_model=tokens.Token,
    tags=["user"],
)
async def register(userInfo: UserIn):
    # ? check format for username, password, email

    # ? create new user
    await register_user(userInfo)

    # * check access token
    access_token_Expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = tokens.create_access_token(
        data={"sub": userInfo.username}, expires_delta=access_token_Expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
