from lib.db import user, db
from typing import List
from pydantic import BaseModel

# ! CLASSES


class HomeInvite(BaseModel):
    id: str
    expiry: str


class Home(BaseModel):
    id: str
    name: str
    residents: List[str]
    chores: List[str]
    creator: str
    invite_link: HomeInvite | None = None


class HomeIn(BaseModel):
    name: str
    residents: List[str] | None = None
    chores: List[str] | None = None


class HomeUpdate(BaseModel):
    name: str | None = None


# ! HELPER


async def get_home_by_creator_and_name(
    container, creator: str, name: str
) -> Home | None:
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


# ! OTHER


async def create_home(home: HomeIn, user: user.User):
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
            },
            enable_automatic_id_generation=True,
        )

        return Home(**res)


async def update_home(
    homeUpdate: HomeUpdate, creator: str, house_name: str, user: user.User
):
    async with db.get_client() as client:
        container_homes = await db.get_or_create_container(client, "homes")

        # home_res = await container_homes.read_item(id, partition_key=id)
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

        homes = [Home(**h) async for h in home_res]
        if len(homes) == 0:
            raise HTTPException(404)

        home = homes[0]
        home.name = home.name if homeUpdate.name == None else homeUpdate.name
        return Home(**await container_homes.upsert_item(home.__dict__))


async def get_homes(user: user.User):
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


async def get_home(id: str):
    async with db.get_client() as client:
        container = await db.get_or_create_container(client, "homes")

        res = await container.read_item(id, partition_key=id)

        return Home(**res)


async def delete_home(id: str, user: user.User):
    async with db.get_client() as client:
        container = await db.get_or_create_container(client, "homes")

        res = await container.read_item(id, partition_key=id)

        if res["creator"] == user.username:
            await container.delete_item(id, partition_key=id)
        else:
            raise HTTPException(401, "Not the creator")


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
    creator: str, house_name: str, user: user.User, link_alive_time_hours: int = 24
):
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
            return home.invite_link.id

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

        home.invite_link = HomeInvite(id=hasher.hexdigest(), expiry=expiry)
        dic = home.__dict__
        dic["invite_link"] = home.invite_link.__dict__

        await container.upsert_item(dic)

        return home.invite_link.id


async def join_home_via_invite_link(
    home_creator: str, home_name: str, invite_id: str, user: user.User
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

        awaited_homes = [Home(**h) async for h in homes]
        if len(awaited_homes) == 0:
            raise HTTPException(404, detail="Invite link not found")

        home: Home = awaited_homes[0]
        if home.invite_link.expiry < datetime.now().isoformat():
            raise HTTPException(400, detail="Invalid invite link")

        if user.username in home.residents:
            raise HTTPException(400, detail="You are already in this home")

        home.residents.append(user.username)
