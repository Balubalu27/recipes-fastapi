from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import status

from recipes.models.recipes import RecipeCreate
from recipes.tables import Recipe
from recipes.database import get_session


class RecipesService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get_list(self, user_id: int) -> list[Recipe]:
        request = select(Recipe).filter_by(author_id=user_id).order_by(Recipe.id)
        recipes = await self.session.execute(request)
        return recipes.scalars().all()

    async def create(self, user_id: int, recipe_data: RecipeCreate) -> Recipe:
        recipe = Recipe(
            **recipe_data.dict(),
            author_id=user_id
        )
        self.session.add(recipe)
        await self.session.commit()
        return recipe
