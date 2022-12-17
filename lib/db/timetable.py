from lib.db import user, home as homeDB, db, chores
from fastapi import HTTPException


# async def get_or_generate_timetable(home_creator: str, home_name: str, caller: str):
#     home = await homeDB.get_home_by_creator_and_name(home_creator, home_name)
#     if home is None:
#         raise HTTPException(404)

#     if caller not in ho

#     async with db.get_client() as client:


async def generate_timetable(home_creator: str, home_name: str):
    home = await homeDB.get_home_by_creator_and_name(home_creator, home_name)
    if home is None:
        raise HTTPException(404)

    async with db.get_client() as client:
        chore_container = db.get_or_create_container(client, "chores")
        user_container = db.get_or_create_container(client, "users")
        chores = sorted(
            [chores.Chore(**await chore_container.read_item(c)) for c in home.chores],
            key=lambda c: c.expected_time,
            reverse=True,
        )
        residents = [
            (user.User(**await user_container.read_item(u)), 0) for u in home.residents
        ]

        timetable = homeDB.Timetable(house_id=home.id, tasks=[])

        # TODO sort by chore score

        for c in chores:
            residents = sorted(residents, key=lambda u: u[1])
            timetable.tasks.append(
                homeDB.TimetabledChore(chore_id=c.id, user_id=residents[0][0].id)
            )
            residents[0][1] += c.expected_time

        print(timetable)
