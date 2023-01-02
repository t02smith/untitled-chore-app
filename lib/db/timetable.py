from lib.db import user as userDB, home as homeDB, db, chores, types
from fastapi import HTTPException
from datetime import datetime, timedelta
from starlette.responses import RedirectResponse

async def get_or_generate_timetable(home_creator: str, home_name: str, caller: types.User) -> types.Timetable:
    home = await homeDB.get_home_by_creator_and_name(home_creator, home_name, caller)
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
      residents[0][1] += c.expected_time # assigns chores to users
    
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
  
  
async def complete_task(username: str, house_name: str, chore_id: str, user: types.User):
  home = await homeDB.get_home_by_creator_and_name(username, house_name, user)
  user = await userDB.get_user_by_username(username)
  
  async with db.get_client() as client:
    container = await db.get_or_create_container(client, "timetables")
    timetable = await get_homes_timetable(home.id)
    if timetable.end < datetime.now().isoformat():
      return RedirectResponse(url=f"/api/v1/{username}/{house_name}/timetable", status_code=302)
    
    chore = list(filter(lambda t: t.chore_id == chore_id, timetable.tasks))
    if len(chore) == 0:
      raise HTTPException(404, detail=f"Chore with id {chore_id} not found in this timetable")
    
    chore = chore[0]
    if chore.user_id != user.username:
      raise HTTPException(403, detail=f"Chore with id {chore_id} is not assigned to user {user.username}")
    
    if chore.complete:
      raise HTTPException(400, detail="This chore is already complete")
    
    chore.complete = True
    #await userDB.update_user(user, )
    #TODO: implement increase user score based on chore score

    await container.upsert_item({
      "id": timetable.id,
      "home_id": timetable.home_id,
      "start": timetable.start,
      "end": timetable.end,
      "tasks": list(map(lambda t: t.__dict__, timetable.tasks)) 
    })
    
    return chore
    