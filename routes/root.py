from fastapi import APIRouter, Depends, HTTPException, Response
from routes import chores, homes
from routes.username import root as username
from lib.db import types, db, user as userDB, timetable
from lib.auth.user import get_current_active_user
from lib.auth import tokens, user as userAuth, auth
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from lib import err


router = APIRouter(prefix="/api/v1")
router.include_router(chores.router)
router.include_router(username.router)
router.include_router(homes.router)

@router.post(
    "/login",
    description="Login using an existing account to untitled-chore-api",
    tags=["user", "auth"],
    status_code=201,
    responses={
        400: {"description": "Invalid username or password", "model": err.HTTPError},
        401: {"description": "Incorrect username or password", "model": err.HTTPError},
    },
)
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    if not types.User.username_valid(form_data.username):
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
    
    response.set_cookie(key="access_token", value=access_token)
    return {"access_token": access_token, "token_type": "bearer", "user": user.to_UserOut()}


@router.post(
    "/register",
    description="Register a new user to untitled-chore-api",
    tags=["user", "auth"],
    status_code=201,
    responses={
        400: {
            "description": "Invalid user details or user already exists",
            "model": err.HTTPError,
        }
    },
)
async def register(userInfo: types.UserIn, response: Response):
    # ? check format for username, password, email
    if not all(
        [types.User.username_valid(userInfo.username), types.User.email_valid(userInfo.email)]
    ):
        raise HTTPException(
            400, detail="Invalid format for username, email or password"
        )

    # ? create new user
    new_user = await userDB.register_user(userInfo)

    # * check access token
    access_token_Expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = tokens.create_access_token(
        data={"sub": userInfo.username}, expires_delta=access_token_Expires
    )
    
    response.set_cookie(key="access_token", value=access_token)
    return {"access_token": access_token, "token_type": "bearer", "user": new_user}

@router.get(
  "/me",
  response_model=types.UserOut,
  status_code=200,
  tags=["user"]
)
async def get_user_info(user: types.User = Depends(get_current_active_user)):
  return user.to_UserOut()


@router.get(
    "/me/timetable",
    tags=["timetable"],
    description="Returns the user's timetable that includes every household.",
    status_code=200,
    response_model=types.UserTimetable,
    responses={
      403: {"message": "A user tries to access someone else's timetable", "model": err.HTTPError}
    }
)
async def get_user_timetable(
    user: types.User = Depends(get_current_active_user)
):      
    return await timetable.get_users_timetable(user)
  
@router.put(
    "/me",
    description="Update a user's information",
    tags=["user"],
    response_model=types.UserOut,
    status_code=200,
    responses={
        403: {"message": "User not authorized to change this user's details","model": err.HTTPError,}
    },
)
async def update_user_info(
    updated: types.UserUpdate,
    user: types.User = Depends(get_current_active_user),
):
    return await userDB.update_user(user, updated)