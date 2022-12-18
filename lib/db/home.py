from fastapi import HTTPException
from lib.db import user, db, types, chores
from pydantic import BaseModel
from datetime import datetime, timedelta
from random import randint
from hashlib import sha1

# * GETTERS


async def get_home_by_creator_and_name(
    creator: str,
    house_name: str,
    caller: types.User,
    fetch_chores_and_residents: bool = False,
) -> types.Home | types.HomeFull | None:
  async with db.get_client() as client:
    home_container = await db.get_or_create_container(client, "homes")
    home_query_res = [h async for h in home_container.query_items("""
      SELECT TOP 1 *
      FROM homes h
      WHERE h.name=@home_name AND h.creator=@creator
      """, 
      parameters=[{"name": "@home_name", "value": house_name},
                  {"name": "@creator", "value": creator}])]
    
    if len(home_query_res) == 0:
      raise HTTPException(404, detail=f"Home {creator}/{house_name} not found")
    
    home = types.Home(**home_query_res[0])
    if caller.username != home.creator or caller.username not in home.residents:
      raise HTTPException(403, detail="You do not have permission to view this home")
    
    if not fetch_chores_and_residents:
      return home
    
    return types.HomeFull(
      id=home.id, 
      name=home.name,
      creator=home.creator,
      residents=await user.get_users_by_username_from_list(home.residents),
      chores=await chores.get_chores_by_id_from_list(home.chores),
      invite_link=home.invite_link
    )

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
            }, enable_automatic_id_generation=True
        )

        return types.Home(**res)


async def update_home(
    homeUpdate: types.HomeUpdate, creator: str, house_name: str, user: types.User
):
    async with db.get_client() as client:
        container_homes = await db.get_or_create_container(client, "homes")
        home = await get_home_by_creator_and_name(creator, house_name, user)
        home.name = home.name if homeUpdate.name == None else homeUpdate.name
        return types.Home(**await container_homes.upsert_item(home.__dict__))


async def get_users_homes(user: types.User):
    async with db.get_client() as client:
        container = await db.get_or_create_container(client, "homes")

        res = container.query_items(
          """
            SELECT *
            from homes h
            WHERE ARRAY_CONTAINS (h['residents'], @username)
          """, parameters=[{"name": "@username", "value": user.username}],
        )

        return [types.Home(**h) async for h in res]


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

        if (home.invite_link is not None
            and datetime.now().isoformat() < home.invite_link.expiry):
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
