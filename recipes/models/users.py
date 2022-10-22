from datetime import datetime

from pydantic import BaseModel

from recipes.models.recipes import Recipe


class User(BaseModel):
    id: int
    username: str
    recipes: list[Recipe]
    # favorites = Column() - ManyToMany на рецепты
    is_active: bool
    created_at: datetime
    last_updated: datetime

    class Config:
        orm_mode = True
