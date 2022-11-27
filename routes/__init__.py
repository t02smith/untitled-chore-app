from fastapi import APIRouter, Depends
from routes.chores import router as chores
from routes.house import router as house
from routes.username import router as username
from lib.auth.user import get_current_user
from lib.db.db import get_or_create_database
from lib.db.user import UserIn
from lib.auth import tokens, user as userAuth, auth
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/v1")
router.include_router(chores)
router.include_router(house)
router.include_router(username)


@router.post("/login", response_model=tokens.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await userAuth.authenticate_user(form_data.username, form_data.password)
    if not user:
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


@router.post("/register", response_model=tokens.Token)
async def register(userInfo: UserIn):
    # ? check format for username, password, email

    # ? check username and email aren't taken

    # ? create new user
    err = await register_user(userInfo)
    if err is not None:
        # !
        raise HTTPException(
            status_code=400,
            detail=err,
        )

    # * check access token
    access_token_Expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = tokens.create_access_token(
        data={"sub": userInfo.username}, expires_delta=access_token_Expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
