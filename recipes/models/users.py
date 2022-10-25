from pydantic import BaseModel

from recipes.models.recipes import Recipe


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class UserWithRecipes(User):
    recipes_count: int
