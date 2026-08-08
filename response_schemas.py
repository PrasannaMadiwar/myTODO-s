from pydantic import BaseModel, Field
import datetime

class UserResponse(BaseModel):
    id: int
    username: str
    user_email : str

    class Config:
        orm_mode = True

class TodoResponse(BaseModel):
    id: int
    title: str
    time: datetime.datetime
    is_completed: bool

    class Config:
        orm_mode = True
