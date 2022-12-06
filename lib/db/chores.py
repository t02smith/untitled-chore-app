from pydantic import BaseModel
from lib.db import db, user


class Chore(BaseModel):
    id: str
    author: str
    name: str
    expected_time: int
    description: str
    public: bool


class ChoreIn(BaseModel):
    name: str
    expected_time: int
    description: str
    public: bool


async def create_chore(chore: ChoreIn, user: user.User) -> Chore:
    async with db.get_client() as client:
        container = await db.get_or_create_container(client, "chores")
        chore = await container.create_item(
            {
                "name": chore.name,
                "expected_time": chore.expected_time,
                "description": chore.description,
                "public": chore.public,
                "author": user.username,
            },
            enable_automatic_id_generation=True,
        )

        return Chore(**chore)


async def get_chores_from_user(username: str, include_private: bool = False):
    async with db.get_client() as client:
        container = await db.get_or_create_container(client, "chores")
        chores_res = container.query_items(
            f"""
        SELECT c.id, c.name, c.author, c.expected_time, c.description, c.public
        FROM chores c
        WHERE c.author=@username {'' if include_private else 'AND c.public'}
      """,
            parameters=[{"name": "@username", "value": username}],
        )

        return [Chore(**c) async for c in chores_res]


async def get_chore_by_id(id: str, username: str) -> Chore:
    async with db.get_client() as client:
        container = await db.get_or_create_container(client, "chores")
        chores_res = container.query_items(
            """
            SELECT c.id, c.name, c.author, c.expected_time, c.description, c.public
            FROM chores c
            WHERE (c.author=@username OR c.public) AND c.id=@id
          """,
            parameters=[
                {"name": "@username", "value": username},
                {"name": "@id", "value": id},
            ],
        )

        return [Chore(**c) async for c in chores_res][0]


async def update_chore(id: str, chore: ChoreIn, username: str):
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
                "description": chore.description
                if len(chore.description) > 0
                else old.description,
                "public": chore.public,
                "author": old.author,
            }
        )

        return Chore(**res)
