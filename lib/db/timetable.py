from lib.db import user as userDB, home as homeDB, db, chores, types
from fastapi import HTTPException
from datetime import datetime, timedelta
from starlette.responses import RedirectResponse
from typing import List

async def _generate_timetable(home_creator: str, home_name: str, caller: types.User, home: types.Home, chore_objs: List[types.Chore]) -> types.Timetable:
    sorted_chores = sorted(chore_objs, key=lambda c: c.score, reverse=True)
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
      timetable.tasks.append(types.TimetabledChore(chore_id=c.id, user_id=residents[0][0], score=c.score))
      residents[0][1] += c.expected_time
      
    return timetable

async def get_or_generate_timetable(home_creator: str, home_name: str, caller: types.User, regenerate: bool) -> types.TimetableOut:
    home = await homeDB.get_home_by_creator_and_name(home_creator, home_name, caller)
    existing_timetable = await get_homes_timetable(home.id)
    
    # ? timetable exists and is still in date
    if existing_timetable is not None:
      if existing_timetable.end > datetime.now().isoformat() and not regenerate:
        return await timetable_to_timetableOut(existing_timetable)
      else:
        for resident in await userDB.get_users_by_username_from_list(home.residents):
          await userDB.new_user_score(resident)
    
    chore_objs = await chores.get_chores_by_id_from_list(home.chores)
    
    # ? generate new timetable
    timetable = await _generate_timetable(home_creator, home_name, caller, home, chore_objs)
    
    # ? write timetable to database
    async with db.get_client() as client:
      container = await db.get_or_create_container(client, "timetables")
      
      if existing_timetable is not None:
        await container.delete_item(existing_timetable.id, existing_timetable.id)
      
      return await timetable_to_timetableOut(types.Timetable(**await container.create_item({
          "home_id": timetable.home_id,
          "start": timetable.start,
          "end": timetable.end,
          "tasks": list(map(lambda t: t.__dict__, timetable.tasks)) 
      }, enable_automatic_id_generation=True)), chore_objs=chore_objs)    
  
async def timetable_to_timetableOut(timetable: types.Timetable, chore_objs: List[types.Chore] = None) -> types.TimetableOut:
  if chore_objs is None:
    chore_objs = await chores.get_chores_by_id_from_list(list(map(lambda t: t.chore_id, timetable.tasks)))
    
  tasks = []
  for task in timetable.tasks:
    chore_ls = list(filter(lambda c: c.id == task.chore_id, chore_objs))
    if len(chore_ls) != 0:
      tasks.append(types.TimetabledChoreOut(chore=chore_ls[0], assigned_to=task.user_id, complete=task.complete, score=chore_ls[0].score))
                    
      
  return types.TimetableOut(
    start=timetable.start,
    end=timetable.end,
    tasks=tasks
  )
      
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
      home = list(filter(lambda h: h.id == t.home_id, homes))[0]
      
      userTimetables.tasks[f"{home.creator}/{home.name}"] = list(map(
        lambda task: types.UserTimetableChore(chore_id=task.chore_id, complete=task.complete), 
        filter(lambda t: t.user_id == user.username, t.tasks)
      ))
      
    return userTimetables
  
  
async def complete_task(username: str, house_name: str, chore_id: str, user: types.User):
  home = await homeDB.get_home_by_creator_and_name(username, house_name, user)
  user = await userDB.get_user_by_username(user.username)
  
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
    user.scores.current_week += chore.score
    
    user_container = await db.get_or_create_container(client, "users")
    await user_container.upsert_item(user.to_json())
    

    await container.upsert_item({
      "id": timetable.id,
      "home_id": timetable.home_id,
      "start": timetable.start,
      "end": timetable.end,
      "tasks": list(map(lambda t: t.__dict__, timetable.tasks)) 
    })
    
    return chore
    