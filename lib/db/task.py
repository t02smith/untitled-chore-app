from pydantic import BaseModel


class Task(BaseModel):
    user: str
    chore: str
    complete: bool = False
