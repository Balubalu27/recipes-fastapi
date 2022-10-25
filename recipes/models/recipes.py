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
    photo_link: str


class Recipe(RecipeBase):
    id: int
    is_active: bool
    author_id: int
    created_at: datetime
    updated_at: datetime
    likes: int

    class Config:
        orm_mode = True


class RecipeCreate(RecipeBase):
    cooking_steps: str

    class Config:
        orm_mode = True


class RecipeShow(Recipe):
    cooking_steps: str
