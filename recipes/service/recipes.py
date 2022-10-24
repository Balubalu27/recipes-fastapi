from fastapi import Depends
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import status

from recipes.models.recipes import RecipeCreate
from recipes.models.users import User
from recipes.service.auth import check_user_status, check_admin_permission
from recipes.service.exceptions import not_found_exception
from recipes.tables import Recipe
from recipes.database import get_session


class RecipesService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get_all_recipes(self, user: User) -> list[Recipe]:
        check_user_status(user)
        request = select(Recipe) \
            .filter_by(is_active=True)\
            .order_by(Recipe.id)
        recipes = await self.session.execute(request)
        return recipes.scalars().all()

    async def get_my_recipes(self, user: User) -> list[Recipe]:
        check_user_status(user)
        request = select(Recipe)\
            .filter_by(is_active=True, author_id=user.id)\
            .order_by(Recipe.id)
        recipes = await self.session.execute(request)
        return recipes.scalars().all()

    async def get_recipe(self, user: User, id: int) -> Recipe:
        check_user_status(user)
        request = select(Recipe).where(Recipe.id == id)
        recipe = await self.session.execute(request)
        result = recipe.scalars().first()
        if not result:
            raise not_found_exception
        return result

    async def create(self, user: User, recipe_data: RecipeCreate) -> Recipe:
        check_user_status(user)
        recipe = Recipe(
            **recipe_data.dict(),
            author_id=user.id
        )
        self.session.add(recipe)
        await self.session.commit()
        return recipe

    async def change_status(self, user: User, recipe_status: bool, id: int):
        check_admin_permission(user)
        query = select(Recipe).where(Recipe.id == id)
        result = await self.session.execute(query)
        recipe = result.scalars().first()
        if not recipe:
            raise not_found_exception
        recipe.is_active = recipe_status
        await self.session.commit()
        return {'detail': f'Recipe id={id} was successfuly updated'}
