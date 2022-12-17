from lib.db import user, home as homeDB, db, chores, types
from fastapi import HTTPException
from datetime import datetime, timedelta

async def get_or_generate_timetable(home_creator: str, home_name: str, caller: types.User) -> types.TimetableOut:
    home = await homeDB.get_home_by_creator_and_name(home_creator, home_name, caller, fetch_chores_and_residents=True)
    if home is None:
        raise HTTPException(404) 

    if home.timetable is not None and home.timetable.end > datetime.now():
      return home.timetable
    
    chores = sorted(home.chores, key=lambda c: c.expected_time, reverse=True)
    residents = list(map(lambda u: [u.username, 0], home.residents))
    timetable = types.Timetable(id=0, house_id=home.id, tasks=[], start=datetime.now(), end=datetime.now()+timedelta(days=7))
    for c in chores:
      residents = sorted(residents, key=lambda u: u[1]) # TODO sort by chore score
      timetable.tasks.append(types.TimetabledChore(chore_id=c.id, user_id=residents[0][0]))
      residents[0][1] += c.expected_time
      
    home.timetable = timetable
    return timetable
