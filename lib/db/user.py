from pydantic import BaseModel
from lib.db.db import get_or_create_container, get_client
from lib.auth.auth import pwd_context
import re


class User(BaseModel):
    id: str
    username: str
    password: str
    email: str
    first_name: str
    surname: str
    disabled: bool

    @staticmethod
    def username_valid(username: str):
        return re.search("[\\d\\w\\-_]{7,15}", username) is not None

    @staticmethod
    def email_valid(email: str):
        return re.search("^[\\w\\-\\.]+@([\\w-]+\\.)+[\\w-]{2,4}$", email)


class UserIn(BaseModel):
    username: str
    password: str
    email: str
    first_name: str
    surname: str


class UserUpdate(BaseModel):
    password: str | None = None
    first_name: str | None = None
    surname: str | None = None


class UserOut(BaseModel):
    username: str
    email: str
    first_name: str
    surname: str

class UserOutPublic(BaseModel):
  username: str
  first_name: str

async def get_user_by_username(username: str) -> User | None:
    async with get_client() as client:
        container = await get_or_create_container(client, "users")

        res = container.query_items(
            query="SELECT TOP 1 * FROM users u WHERE u.username=@username",
            parameters=[{"name": "@username", "value": username}],
        )
        items = [item async for item in res]
        if len(items) == 0:
            return None

        return User(**items[0])


async def register_user(user: UserIn):
    async with get_client() as client:
        container = await get_or_create_container(client, "users")

        user_exists = container.query_items(
            """
          SELECT u.id
          FROM users u
          WHERE u.email=@email OR u.username=@username
          """,
            paramters=[
                {"name": "@username", "value": user.username},
                {"name": "@email", "value": user.email},
            ],
        )

        res = UserOut(
            **await container.create_item(
                {
                    "username": user.username,
                    "password": pwd_context.hash(user.password),
                    "first_name": user.first_name,
                    "surname": user.surname,
                    "email": user.email,
                    "disabled": False,
                },
                enable_automatic_id_generation=True,
            )
        )


async def update_user(old, updated: UserUpdate) -> UserOut:
    async with get_client() as client:
        container = await get_or_create_container(client, "users")
        return UserOut(
            **await container.upsert_item(
                {
                    "id": old.id,
                    "username": old.username,
                    "password": old.password
                    if updated.password is None
                    else pwd_context.hash(updated.password),
                    "email": old.email,
                    "first_name": old.first_name
                    if updated.first_name is None
                    else updated.first_name,
                    "surname": old.surname
                    if updated.surname is None
                    else updated.surname,
                    "disabled": old.disabled,
                }
            )
        )
