from pydantic import BaseModel
from lib.db import db, user, types
from typing import List


async def create_chore(chore: types.ChoreIn, user: types.User) -> types.Chore:
    async with db.get_client() as client:
        container = await db.get_or_create_container(client, "chores")
        chore = await container.create_item(
            {
                "name": chore.name,
                "expected_time": chore.expected_time,
                "difficulty": chore.difficulty,
                "score": chore.expected_time * chore.difficulty,
                "description": chore.description,
                "public": chore.public,
                "author": user.username,
                "room": chore.room.__dict__,
            },
            enable_automatic_id_generation=True,
        )

        return types.Chore(**chore)


async def get_chores_from_user(username: str, include_private: bool = False):
    async with db.get_client() as client:
        container = await db.get_or_create_container(client, "chores")
        chores_res = container.query_items(
            f"""
        SELECT c.id, c.name, c.author, c.expected_time, c.difficulty, c.description, c.public, c.room
        FROM chores c
        WHERE c.author=@username {'' if include_private else 'AND c.public'}
      """,
            parameters=[{"name": "@username", "value": username}],
        )

        return [c async for c in chores_res]


async def get_chore_by_id(id: str) -> types.Chore | None:
    res = await get_chores_by_id_from_list([id])
    return None if len(res) == 0 else res[0]


async def get_chores_by_id_from_list(chores: List[str]) -> List[types.Chore]:
    async with db.get_client() as client:
        container = await db.get_or_create_container(client, "chores")
        return [
            types.Chore(**c)
            async for c in container.query_items(
                """
      SELECT *
      FROM chores c
      WHERE ARRAY_CONTAINS(@chores, c.id) 
      """,
                parameters=[{"name": "@chores", "value": chores}],
            )
        ]


async def update_chore(id: str, chore: types.ChoreIn, username: str):
    async with db.get_client() as client:
        container = await db.get_or_create_container(client, "chores")
        old = await get_chore_by_id(id, username)

        res = await container.upsert_item(
            {
                "id": id,
                "name": chore.name if len(chore.name) > 0 else old.name,
                "expected_time": chore.expected_time
                if chore.expected_time != -1
                else old.expected_time,
                "difficulty": chore.difficulty
                if chore.difficulty != -1
                else old.difficulty,
                "description": chore.description
                if len(chore.description) > 0
                else old.description,
                "public": chore.public,
                "author": old.author,
            }
        )

        return types.Chore(**res)


async def default_chores():
    async with db.get_client() as client:
        container = await db.get_or_create_container(client, "chores")
        return [
            c
            async for c in container.query_items(
                """
        SELECT TOP 6 *
        FROM chores c
        WHERE c.id LIKE 'default-%'
      """
            )
        ]
