from datetime import datetime, timedelta
from pydantic import BaseModel
from jose import jwt
from lib.auth import auth


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    copy = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)

    copy.update({"exp": expire})
    access_token = jwt.encode(copy, auth.SECRET_KEY, algorithm=auth.ALGORITHM)
    return access_token
