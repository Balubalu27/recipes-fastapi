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


class Recipe(BaseModel):
    id: int
    title: str
    author_id: int
    dish_type: DishType
    description: str | None
    cooking_steps: str
    photo_link: str
    # likes = Column()
    # hashtags = Column()
    is_active: bool
    created_at: datetime
    last_updated: datetime

    class Config:
        orm_mode = True
    