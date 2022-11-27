from pydantic import BaseModel
from lib.db.db import get_or_create_container, get_client
from lib.auth.auth import pwd_context


class User(BaseModel):
    id: str
    username: str
    password: str
    email: str
    first_name: str
    surname: str
    disabled: bool


class UserIn(BaseModel):
    username: str
    password: str
    email: str
    first_name: str
    surname: str


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
        await container.create_item(
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
