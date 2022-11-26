from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from lib.auth import user as userAuth
from lib.auth import auth, tokens
from datetime import timedelta
from lib.db.user import UserDB, register_user

router = APIRouter(prefix="/users")


@router.get("/me")
async def me(user: userAuth.User = Depends(userAuth.get_current_active_user)):
    return user


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
async def register(user: UserDB):
    # ? check correct fields are included

    # ? check username and password

    # ? check username and email aren't taken

    # ? create new user
    register_user(user)
