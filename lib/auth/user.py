from fastapi import Depends
from lib.db.user import get_user, User
from fastapi import HTTPException
from datetime import datetime, timedelta
from jose import JWTError, jwt
from lib.auth import tokens, auth


async def get_current_user(token: str = Depends(auth.oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = tokens.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        # TODO change to redirect
        raise HTTPException(status_code=400, detail="Inactive user")
    return User(**current_user.__dict__)


# * passwords


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return user


def verify_password(plaintext, hashed):
    return auth.pwd_context.verify(plaintext, hashed)


def get_password_hash(password):
    return auth.pwd_context.hash(password)
