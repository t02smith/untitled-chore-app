from pydantic import BaseModel

fake_users_db = {
    "tom": {
        "username": "tom",
        "first_name": "Tom",
        "surname": "smith",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


class User(BaseModel):
    username: str
    email: str | None = None
    first_name: str | None = None
    surname: str | None = None
    disabled: bool | None = None


class UserDB(User):
    hashed_password: str


def get_user(username: str) -> UserDB | None:
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return UserDB(**user_dict)
