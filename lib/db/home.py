from fastapi import HTTPException
from lib.db import user, db, types
from pydantic import BaseModel
from datetime import datetime, timedelta
from random import randint
from hashlib import sha1


async def get_home_by_creator_and_name(
    creator: str, name: str, container=None
) -> types.Home | None:
    async def func():

        res = [
            Home(**h)
            async for h in container.query_items(
                """
      SELECT TOP 1 *
      FROM homes h
      WHERE h.name=@name AND h.creator=@creator
      """,
                parameters=[
                    {"name": "@name", "value": name},
                    {"name": "@creator", "value": creator},
                ],
            )
        ]

        return None if len(res) == 0 else res[0]

    if container is not None:
        return await func()
    else:
        async with db.get_client() as client:
            container = await db.get_or_create_container(client, "homes")
            return await func()


async def create_home(home: types.HomeIn, user: types.User):
    async with db.get_client() as client:
        container_homes = await db.get_or_create_container(client, "homes")
        container_users = await db.get_or_create_container(client, "users")

        users_res = container_users.query_items(
            """
      SELECT u.username
      FROM users u
      WHERE ARRAY_CONTAINS(@username, u.username)
      """,
            parameters=[{"name": "@username", "value": home.residents}],
        )

        res = [u["username"] async for u in users_res]

        res.append(user.username)
        res = await container_homes.create_item(
            {
                "name": home.name,
                "residents": res,
                "chores": [] if home.chores is None else home.chores,
                "creator": user.username,
                "invite_link": None,
            },
            enable_automatic_id_generation=True,
        )

        return Home(**res)


async def update_home(
    homeUpdate: types.HomeUpdate, creator: str, house_name: str, user: types.User
):
    async with db.get_client() as client:
        container_homes = await db.get_or_create_container(client, "homes")

        home_res = container_homes.query_items(
            """
      SELECT * 
      FROM homes h
      WHERE h.creator=@creator AND h.name=@name
      """,
            parameters=[
                {"name": "@creator", "value": creator},
                {"name": "@name", "value": house_name},
            ],
        )

        homes = [types.Home(**h) async for h in home_res]
        if len(homes) == 0:
            raise HTTPException(404)

        home = homes[0]
        home.name = home.name if homeUpdate.name == None else homeUpdate.name
        return types.Home(**await container_homes.upsert_item(home.__dict__))


async def get_homes(user: types.User):
    async with db.get_client() as client:
        container = await db.get_or_create_container(client, "homes")

        res = container.query_items(
            """
      SELECT h.name
      from homes h
      WHERE ARRAY_CONTAINS (h['residents'], @username)
      """,
            parameters=[{"name": "@username", "value": user.username}],
        )

        res2 = [r["name"] async for r in res]
        return res2


async def delete_home(id: str, user: types.User):
    async with db.get_client() as client:
        container = await db.get_or_create_container(client, "homes")

        res = await container.read_item(id, partition_key=id)

        if res["creator"] == user.username:
            await container.delete_item(id, partition_key=id)
        else:
            raise HTTPException(401, "Not the creator")


async def create_invite_link(
    creator: str, house_name: str, user: types.User, link_alive_time_hours: int = 24
) -> types.HomeInvite:
    async with db.get_client() as client:
        container = await db.get_or_create_container(client, "homes")

        # Check home exists
        home = await get_home_by_creator_and_name(container, creator, house_name)
        if home is None:
            raise HTTPException(404)

        if (
            home.invite_link is not None
            and datetime.now().isoformat() < home.invite_link.expiry
        ):
            return home.invite_link

        # generate required link values
        nonce = randint(0, 100000000000000000000)
        created_at = datetime.now()
        expiry = (created_at + timedelta(hours=link_alive_time_hours)).isoformat()

        # hash values
        hasher = sha1()
        hasher.update(str(nonce).encode())
        hasher.update(expiry.encode())
        hasher.update(created_at.isoformat().encode())
        hasher.update(home.id.encode())

        home.invite_link = types.HomeInvite(id=hasher.hexdigest(), expiry=expiry)
        dic = home.__dict__
        dic["invite_link"] = home.invite_link.__dict__

        await container.upsert_item(dic)
        print(home.invite_link)
        return home.invite_link


async def join_home_via_invite_link(
    home_creator: str, home_name: str, invite_id: str, user: types.User
):
    async with db.get_client() as client:
        container = await db.get_or_create_container(client, "homes")

        homes = container.query_items(
            """
      SELECT TOP 1 *
      FROM homes h
      WHERE h.invite_link.id=@id AND h.name=@name AND h.creator=@creator
      """,
            parameters=[
                {"name": "@id", "value": invite_id},
                {"name": "@name", "value": home_name},
                {"name": "@creator", "value": home_creator},
            ],
        )

        awaited_homes = [types.Home(**h) async for h in homes]
        if len(awaited_homes) == 0:
            raise HTTPException(404, detail="Invite link not found")

        home: Home = awaited_homes[0]
        if home.invite_link.expiry < datetime.now().isoformat():
            raise HTTPException(400, detail="Expired invite link")

        if user.username in home.residents:
            raise HTTPException(400, detail="You are already in this home")

        home.residents.append(user.username)
        await container.upsert_item(home.to_json())
