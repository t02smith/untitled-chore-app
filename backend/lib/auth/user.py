from fastapi import Depends
from lib.db import user as userDB, types
from fastapi import HTTPException
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

    user = await userDB.get_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: types.User = Depends(get_current_user),
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return types.User(**current_user.__dict__)


# * passwords


async def authenticate_user(username: str, password: str):
    user = await userDB.get_user_by_username(username)
    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user


def verify_password(plaintext, hashed):
    return auth.pwd_context.verify(plaintext, hashed)
