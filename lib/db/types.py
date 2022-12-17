from pydantic import BaseModel
from typing import List
from datetime import datetime

# ! USER


class User(BaseModel):
    id: str
    username: str
    password: str
    email: str
    first_name: str
    surname: str
    disabled: bool

    @staticmethod
    def username_valid(username: str):
        return re.search("[\\d\\w\\-_]{7,15}", username) is not None

    @staticmethod
    def email_valid(email: str):
        return re.search("^[\\w\\-\\.]+@([\\w-]+\\.)+[\\w-]{2,4}$", email)


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


# ! CHORES


class Chore(BaseModel):
    id: str
    author: str
    name: str
    expected_time: int
    description: str
    public: bool


class ChoreIn(BaseModel):
    name: str
    expected_time: int
    description: str
    public: bool


# ! TIMETABLE

# a chore assigned to a user in a given timetable
class TimetabledChore(BaseModel):
    chore_id: str
    user_id: str
    complete: bool = False


# a timetable for a house for a given week
class Timetable(BaseModel):
    id: str
    house_id: str
    start: datetime
    end: datetime
    tasks: List[TimetabledChore]


class TimetableOut(BaseModel):
    house_name: str
    start: datetime
    end: datetime
    tasks: List[TimetabledChore]


# ! HOME


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
    timetable: Timetable

    def to_json(self):
        dic = self.__dict__
        dic["invite_link"] = (
            None if self.invite_link is None else self.invite_link.__dict__
        )

        return dic


class HomeFull:
    id: str
    name: str
    creator: str
    residents: List[User]
    chores: List[Chore]
    timetable: Timetable
    invite_link: HomeInvite


# ? Home IO classes


class HomeIn(BaseModel):
    name: str
    residents: List[str] | None = None
    chores: List[str] | None = None


class HomeUpdate(BaseModel):
    name: str | None = None
    chores: List[str] | None = None
