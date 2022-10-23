from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from recipes.tables import Recipe
from recipes.database import get_session


class RecipesService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get_list(self) -> list[Recipe]:
        request = select(Recipe).order_by(Recipe.id)
        recipes = await self.session.execute(request)
        return recipes.scalars().all()
