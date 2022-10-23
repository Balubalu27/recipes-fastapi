from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class DishType(str, Enum):
    SALAD = 'Салат'
    FIRST = 'Первое'
    SECOND = 'Второе'
    DESSERT = 'Десерт'
    DRINK = 'Напиток'
    PASTRY = 'Выпечка'


class RecipeBase(BaseModel):
    title: str
    dish_type: DishType
    description: str | None
    cooking_steps: str
    photo_link: str


class Recipe(RecipeBase):
    id: int
    is_active: bool
    author_id: int
    created_at: datetime
    last_updated: datetime
    likes: int

    class Config:
        orm_mode = True


class RecipeCreate(RecipeBase):
    class Config:
        orm_mode = True
