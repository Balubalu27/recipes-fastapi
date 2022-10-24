from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str
