from lib.db import user, db
from typing import List
from pydantic import BaseModel
from datetime import datetime, timedelta
from random import randint
from hashlib import sha1
from fastapi import HTTPException


class HomeInvite(BaseModel):
    id: str
    expiry: datetime


class Home(BaseModel):
    id: str
    name: str
    residents: List[str]
    chores: List[str]
    creator: str
    invite_link: HomeInvite


class HomeIn(BaseModel):
    name: str
    residents: List[str] | None = None
    chores: List[str] | None = None


async def register_home(home: HomeIn, creator: str):
    async with db.get_client() as client:
        container = await db.get_or_create_container(client, "homes")

        if home.residents is None:
            home.residents = []

        home.residents.append(creator)
        await container.create_item(
            {
                "name": home.name,
                "residents": home.residents,
                "chores": [] if home.chores is None else home.chores,
                "creator": creator,
            },
            enable_automatic_id_generation=True,
        )


async def create_invite_link(
    home_id: str, user: user.User, link_alive_time_hours: int = 24
):
    async with db.get_client() as client:
        container = await db.get_or_create_container(client, "homes")

        # Check home exists
        home = Home(**(await container.read_item(home_id, home_id)))
        if home.creator != user.username:
            raise HTTPException(
                403, detail="Only the creator can create a link for a house."
            )

        # generate required link values
        nonce = randint(0, 100000000000000000000)
        created_at = datetime.now()
        expiry = created_at + timedelta(hours=link_alive_time_hours)

        # hash values
        hasher = sha1()
        hasher.update(str(nonce).encode())
        hasher.update(expiry.isoformat().encode())
        hasher.update(created_at.isoformat().encode())
        hasher.update(home_id.encode())

        invite = HomeInvite(id=hasher.hexdigest(), expiry=expiry)

        print(invite)


async def join_home_via_invite_link(invite_id: str, user: user.User):
    async with db.get_client() as client:
        container = await db.get_or_create_container(client, "homes")

        homes = container.query_items(
            """
      SELECT *
      FROM homes h
      WHERE h.invite_link.id=@id
      """,
            parameters=[{"name": "@id", "value": invite_id}],
        )

        awaited_homes = [Home(**h) async for h in homes]
        if len(awaited_homes) == 0:
            raise HTTPException(400, detail="Invalid invite link")

        home: Home = awaited_homes[0]
        if home.invite_link.expiry < datetime.now().isoformat():
            raise HTTPException(400, detail="Invalid invite link")

        home.residents.append(user.username)
