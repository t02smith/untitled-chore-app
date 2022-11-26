from pydantic import BaseModel
from lib.db.db import get_or_create_container, get_client


class User(BaseModel):
    id: str | None = None
    username: str
    email: str | None = None
    first_name: str | None = None
    surname: str | None = None
    disabled: bool | None = None


class UserDB(User):
    hashed_password: str


async def get_user_by_username(username: str) -> UserDB | None:
    async with get_client() as client:
        container = await get_or_create_container(client, "users")

        res = container.query_items(
            query="SELECT TOP 1 * FROM users u WHERE u.username=@username",
            parameters=[{"name": "@username", "value": username}],
        )
        items = [item async for item in res]
        if len(items) == 0:
            return None

        return UserDB(**items[0])


async def register_user(user: UserDB):
  return True
    # async with get_client() as client:
    #     container = await get_or_create_container(client, "users")
    #     await container.create_item(
    #         {
    #             "username": user.username,
    #             "password": user.hashed_password,
    #             "first_name": user.first_name,
    #             "surname": user.surname,
    #             "email": user.email,
    #             "disabled": False,
    #         },
    #         enable_automatic_id_generation=True,
    #     )
