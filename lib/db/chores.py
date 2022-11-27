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


async def create_chore(chore: ChoreIn, user: user.User):
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
