from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
import re
from dataclasses import dataclass
from statistics import mean

# ! USER

# ? User IO

class UserIn(BaseModel):
    username: str
    password: str
    email: str
    first_name: str
    surname: str


class UserUpdate(BaseModel):
    password: str | None = None
    first_name: str | None = None
    surname: str | None = None


class UserOut(BaseModel):
    username: str
    email: str | None = None
    first_name: str
    surname: str | None = None
    score: float
    
# ? User DB

class Score(BaseModel):
    current_week: float
    history: List[float]

class User(BaseModel):
    id: str
    username: str
    password: str
    email: str
    first_name: str
    surname: str
    disabled: bool
    scores: Score

    @staticmethod
    def username_valid(username: str):
        return re.search("[\\d\\w\\-_]{7,15}", username) is not None

    @staticmethod
    def email_valid(email: str):
        return re.search("^[\\w\\-\\.]+@([\\w-]+\\.)+[\\w-]{2,4}$", email)

    def to_UserOut(self) -> UserOut:
      return UserOut(**self.__dict__, score=mean(self.scores.history + [self.scores.current_week]))




# ! CHORES

class Room(BaseModel):
    name: str
    colour: str
    icon: str


class Chore(BaseModel):
    id: str
    author: str
    name: str
    expected_time: int
    difficulty: int
    score: int
    description: str
    public: bool
    room: List[Room]


class ChoreIn(BaseModel):
    name: str
    expected_time: int
    difficulty: int
    description: str
    public: bool
    room: List[Room]

# ! LEADERBOARD
#class Leaderboard(BaseModel):
    


# ! TIMETABLE

# a chore assigned to a user in a given timetable
class TimetabledChore(BaseModel):
    chore_id: str
    user_id: str
    complete: bool = False
    score: float
    
class TimetabledChoreOut(BaseModel):
    chore: Chore
    assigned_to: str
    complete: bool
    score: float

# a timetable for a house for a given week
class Timetable(BaseModel):
    id: str
    home_id: str
    start: str
    end: str
    tasks: List[TimetabledChore]
    
    
class TimetableOut(BaseModel):
    start: str
    end: str
    tasks: List[TimetabledChoreOut]
    
    
class UserTimetableChore(BaseModel):
  chore_id: str
  complete: bool
    
class UserTimetable(BaseModel):
  username: str
  tasks: Dict[str, List[UserTimetableChore]]
  



# ! HOME


class HomeInvite(BaseModel):
    id: str
    link: str
    expiry: str


class Home(BaseModel):
    id: str
    name: str
    residents: List[str]
    chores: List[str]
    creator: str
    invite_link: HomeInvite | None = None

    def to_json(self):
        dic = self.__dict__
        dic["invite_link"] = (
            None if self.invite_link is None else self.invite_link.__dict__
        )

        return dic

@dataclass
class HomeFull:
    id: str
    name: str
    creator: str
    residents: List[User]
    chores: List[Chore]
    timetable: Timetable | None = None
    invite_link: HomeInvite | None = None


# ? Home IO classes


class HomeIn(BaseModel):
    name: str
    chores: List[str] | None = None


class HomeUpdate(BaseModel):
    name: str | None = None
    chores: List[str] | None = None
