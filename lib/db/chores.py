from pydantic import BaseModel
from lib.db import db, user


class Chore:
    id: str
    author_id: str
    name: str
    expected_time: int
    description: str
    public: bool


class ChoreIn(BaseModel):
    name: str
    expected_time: int
    description: str
    public: bool


class ChoreOut(BaseModel):
    id: str
    name: str
    author: str
    expected_time: int
    description: str
    public: bool


async def create_chore(chore: ChoreIn, user: user.User) -> ChoreOut:
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

        return ChoreOut(**chore)


async def get_chores_from_user(username: str):
    async with db.get_client() as client:
        container = await db.get_or_create_container(client, "chores")
        chores_res = container.query_items(
            """
        SELECT c.id, c.name, c.author, c.expected_time, c.description, c.public
        FROM chores c
        WHERE c.author=@username
      """,
            parameters=[{"name": "@username", "value": username}],
        )

        chores = [ChoreOut(**c) async for c in chores_res]
        return chores


async def get_chore_by_id(id: str, username: str):
    async with db.get_client() as client:
        container = await db.get_or_create_container(client, "chores")
        chore_res = container.query_items(
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

        return [ChoreOut(**c) async for c in chores_res][0]
