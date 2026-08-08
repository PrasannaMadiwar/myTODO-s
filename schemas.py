from pydantic import BaseModel, Field
import datetime


class UserBase(BaseModel):
    username : str = Field(...)
    password : str = Field(...)
    user_email : str = Field(...)


class TodoBase(BaseModel):
    title : str = Field(...)
    time : datetime.datetime = Field(...)
    is_completed : bool = Field(default=False)
    
