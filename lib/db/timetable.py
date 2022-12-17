from lib.db import user, home as homeDB, db, chores, types
from fastapi import HTTPException
from datetime import datetime, timedelta

async def get_or_generate_timetable(home_creator: str, home_name: str, caller: types.User) -> types.Timetable:
    home = await homeDB.get_home_by_creator_and_name(home_creator, home_name, caller)
    if home is None:
        raise HTTPException(404) 

    existing_timetable = await get_homes_timetable(home.id)
    if existing_timetable is not None and existing_timetable.end > datetime.now().isoformat():
      return existing_timetable
    
    chore_objs = await chores.get_chores_by_id_from_list(home.chores)
    
    # ? generate new timetable
    sorted_chores = sorted(chore_objs, key=lambda c: c.expected_time, reverse=True)
    residents = list(map(lambda u: [u, 0], home.residents))
    timetable = types.Timetable(
      id="0",
      home_id=home.id, 
      tasks=[], 
      start=datetime.now().isoformat(),
      end=(datetime.now()+timedelta(days=7)).isoformat()
    )
      
    for c in sorted_chores:
      residents = sorted(residents, key=lambda u: u[1]) # TODO sort by chore score
      timetable.tasks.append(types.TimetabledChore(chore_id=c.id, user_id=residents[0][0]))
      residents[0][1] += c.expected_time
    
    # ? write timetable to database
    async with db.get_client() as client:
      container = await db.get_or_create_container(client, "timetables")
      
      if existing_timetable is not None:
        await container.delete_item(existing_timetable.id, existing_timetable.id)
      
      return types.Timetable(**await container.create_item({
          "home_id": timetable.home_id,
          "start": timetable.start,
          "end": timetable.end,
          "tasks": list(map(lambda t: t.__dict__, timetable.tasks)) 
      }, enable_automatic_id_generation=True))
      
    # TODO remove old timetable from database
      
      
async def get_homes_timetable(home_id: str) -> types.Timetable | None:
  async with db.get_client() as client:
    container = await db.get_or_create_container(client, "timetables")
    res = [t async for t in container.query_items(
      """
      SELECT TOP 1 *
      FROM timetables t
      WHERE t.home_id=@home_id
      """, parameters=[{"name": "@home_id", "value": home_id}]
    )]
    
    return None if len(res) == 0 else types.Timetable(**res[0])
  
  
async def get_users_timetable(user: types.User) -> types.UserTimetable:
  homes = await homeDB.get_users_homes(user)
  async with db.get_client() as client:
    container = await db.get_or_create_container(client, "timetables")
    timetables = [types.Timetable(**t) async for t in container.query_items(
      """
      SELECT *
      FROM timetables t
      WHERE ARRAY_CONTAINS(@homes, t.home_id)
      """, parameters=[{"name": "@homes", "value": list(map(lambda h: h.id, homes))}]
    )]
    
    userTimetables = types.UserTimetable(
      username=user.username,
      tasks={}
    )
    
    for t in timetables:
      userTimetables.tasks[t.home_id] = list(map(
        lambda task: types.UserTimetableChore(chore_id=task.chore_id, complete=task.complete), 
        t.tasks
      ))
      
    return userTimetables