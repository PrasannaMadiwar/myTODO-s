from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username : str = Field(...)
    password : str = Field(...)


class TodoBase(BaseModel):
    title : str = Field(...)
    time : str = Field(...)
    is_completed : bool = Field(default=False)
    
