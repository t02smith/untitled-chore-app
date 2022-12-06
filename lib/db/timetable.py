from typing import List
from lib.db import task
from datetime import datetime


class Timetable:
    house: str
    tasks: List[task.Task]
    start_date: datetime
    end_date: datetime
