from pydantic import BaseModel
from lib.db.db import get_or_create_container, get_client
from lib.db import types
from lib.auth.auth import pwd_context
from typing import List

async def get_user_by_username(username: str) -> types.User | None:
    res = await get_users_by_username_from_list([username])
    return None if len(res) == 0 else res[0]

async def get_users_by_username_from_list(usernames: List[str]) -> List[types.User]:
  async with get_client() as client:
    container = await get_or_create_container(client, "users")
    return [types.User(**u) async for u in container.query_items(
      """
      SELECT *
      FROM users u
      WHERE ARRAY_CONTAINS(@usernames, u.username)
      """, parameters=[{"name": "@usernames", "value": usernames}]
    )]

async def register_user(user: types.UserIn):
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

        res = types.UserOut(
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


async def update_user(old, updated: types.UserUpdate) -> types.UserOut:
    async with get_client() as client:
        container = await get_or_create_container(client, "users")
        return types.UserOut(
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
