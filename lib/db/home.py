from datetime import datetime, timedelta
from hashlib import sha1
from random import randint
from lib.db import user, db, types
from typing import List
from pydantic import BaseModel
from fastapi import HTTPException

MAX_HOMES = 5

# * GETTERS


async def get_home_by_creator_and_name(
    creator: str,
    house_name: str,
    caller: types.User,
    fetch_chores_and_residents: bool = False,
    allow_all_users: bool = False,
) -> types.Home | types.HomeFull:
    async with db.get_client() as client:
        home_container = await db.get_or_create_container(client, "homes")
        home_query_res = [
            h
            async for h in home_container.query_items(
                """
      SELECT TOP 1 *
      FROM homes h
      WHERE h.name=@home_name AND h.creator=@creator
      """,
                parameters=[
                    {"name": "@home_name", "value": house_name},
                    {"name": "@creator", "value": creator},
                ],
            )
        ]

        if len(home_query_res) == 0:
            raise HTTPException(404, detail=f"Home {creator}/{house_name} not found")

        home = types.Home(**home_query_res[0])
        if (
            caller.username != home.creator and caller.username not in home.residents
        ) and not allow_all_users:
            raise HTTPException(
                403, detail="You do not have permission to view this home"
            )

        if not fetch_chores_and_residents:
            return home

        return types.HomeFull(
            id=home.id,
            name=home.name,
            creator=home.creator,
            residents=await user.get_users_by_username_from_list(home.residents),
            chores=await chores.get_chores_by_id_from_list(home.chores),
            invite_link=home.invite_link,
        )


async def get_home_residents(creator: str, home_name: str, caller: types.User):
    home = await get_home_by_creator_and_name(creator, home_name, caller)
    return await user.get_users_by_username_from_list(home.residents)


async def create_home(home: types.HomeIn, user: types.User):
    user_homes = list(
        filter(lambda h: h.creator == user.username, await get_users_homes(user))
    )
    if len(user_homes) == MAX_HOMES:
        raise HTTPException(400, detail="Max number of homes already created")

    if home.name in list(map(lambda h: h.name, user_homes)):
        raise HTTPException(400, detail="user already has a home with this name")

    async with db.get_client() as client:
        container_homes = await db.get_or_create_container(client, "homes")
        container_users = await db.get_or_create_container(client, "users")

        res = await container_homes.create_item(
            {
                "name": home.name,
                "residents": [user.username],
                "chores": [] if home.chores is None else home.chores,
                "creator": user.username,
                "invite_link": None,
                "posts": []
            },
            enable_automatic_id_generation=True,
        )

        return types.Home(**res)


async def update_home(
    homeUpdate: types.HomeUpdate, creator: str, house_name: str, user: types.User
):
    async with db.get_client() as client:
        container_homes = await db.get_or_create_container(client, "homes")
        home = await get_home_by_creator_and_name(creator, house_name, user)
        
        for c in homeUpdate.chores:
          if c not in home.chores:
            home.chores.append(c)
        
        return types.Home(**await container_homes.upsert_item(home.__dict__))

async def remove_chores_from_home(homeUpdate: types.HomeUpdate, creator: str, house_name: str, user: types.User):
    async with db.get_client() as client:
        container_homes = await db.get_or_create_container(client, "homes")
        home = await get_home_by_creator_and_name(creator, house_name, user)
        home.chores = list(filter(lambda c: c not in homeUpdate.chores, home.chores))
        
        return types.Home(**await container_homes.upsert_item(home.__dict__))

async def get_users_homes(user: types.User) -> List[types.Home]:
    async with db.get_client() as client:
        container = await db.get_or_create_container(client, "homes")

        res = container.query_items(
            """
            SELECT *
            from homes h
            WHERE ARRAY_CONTAINS (h['residents'], @username)
          """,
            parameters=[{"name": "@username", "value": user.username}],
        )
        return [types.Home(**h) async for h in res]


async def delete_home(creator: str, home_name: str, caller: types.User):
    if caller.username != creator:
        raise HTTPException(
            403, detail="You do not have permission to delete this home"
        )

    home = await get_home_by_creator_and_name(creator, home_name, caller)
    async with db.get_client() as client:
        container = await db.get_or_create_container(client, "homes")
        await container.delete_item(home.id, partition_key=home.id)


async def leave_home(creator: str, home_name: str, caller: types.User):
  if caller.username == creator:
    raise HTTPException(400, detail="You cannot leave a home you created. You can only delete it")
  
  home = await get_home_by_creator_and_name(creator, home_name, caller)
  if caller.username not in home.residents:
    raise HTTPException(400, detail="You are not a resident of this home")
  
  home.residents.remove(caller.username)
  async with db.get_client() as client:
    container = await db.get_or_create_container(client, "homes")
    await container.upsert_item(home.to_json())

async def create_invite_link(
    creator: str, house_name: str, caller: types.User, link_alive_time_hours: int = 24
) -> types.HomeInvite:
    home = await get_home_by_creator_and_name(creator, house_name, caller)
    if (
        home.invite_link is not None
        and datetime.now().isoformat() < home.invite_link.expiry
    ):
        return home.invite_link

    # Create new invite link
    created_at = datetime.now()
    expiry = (created_at + timedelta(hours=link_alive_time_hours)).isoformat()

    hasher = sha1()
    hasher.update(str(randint(0, 999999)).encode())
    hasher.update(expiry.encode())
    hasher.update(created_at.isoformat().encode())
    hasher.update(home.id.encode())
    id = hasher.hexdigest()

    home.invite_link = types.HomeInvite(
        id=id, expiry=expiry, link=f"/api/v1/{creator}/{house_name}/join?invite_id={id}"
    )
    dic = home.__dict__
    dic["invite_link"] = home.invite_link.__dict__

    async with db.get_client() as client:
        container = await db.get_or_create_container(client, "homes")
        await container.upsert_item(dic)

    return home.invite_link


async def join_home_via_invite_link(
    home_creator: str, home_name: str, invite_id: str, caller: types.User
):
    home: types.Home = await get_home_by_creator_and_name(
        home_creator, home_name, caller, allow_all_users=True
    )
    
    if home.invite_link.id != invite_id:
        raise HTTPException(404, detail="Invite link not found")

    if home.invite_link.expiry < datetime.now().isoformat():
        raise HTTPException(400, detail="Invite link has expired")

    if caller.username in home.residents:
        raise HTTPException(400, detail="You are already a resident in this home")

    home.residents.append(caller.username)
    async with db.get_client() as client:
        container = await db.get_or_create_container(client, "homes")
        return types.Home(**await container.upsert_item(home.to_json()))


async def upload_admin_post(creator: str, home_name: str, message: str, caller: types.User):
  if creator != caller.username:
    raise HTTPException(403, detail="You do not have permission to send messages")
  
  home = await get_home_by_creator_and_name(creator, home_name, caller)
  post = types.AdminPost(timestamp=datetime.now().isoformat(), content=message)
  home.posts.append(post)
  home.posts = list(filter(lambda p: (datetime.now() - timedelta(days=7)).isoformat() < p.timestamp , home.posts))
  
  async with db.get_client() as client:
    container = await db.get_or_create_container(client, "homes")
    await container.upsert_item(home.to_json())
    
  return post