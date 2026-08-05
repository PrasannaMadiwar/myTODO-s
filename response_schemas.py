from pydantic import BaseModel, Field

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class TodoResponse(BaseModel):
    id: int
    title: str
    time: str
    is_completed: bool

    class Config:
        orm_mode = True
