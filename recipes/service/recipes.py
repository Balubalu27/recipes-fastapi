from fastapi_pagination import Page, add_pagination, paginate
from fastapi_pagination.ext.sqlalchemy import paginate

from fastapi import Depends
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from recipes.models.recipes import RecipeCreate, DishType
from recipes.models.users import User
from recipes.models import recipes
from recipes.service.auth import check_user_status, check_admin_permission
from recipes.service.exceptions import not_found_exception
from recipes.tables import Recipe
from recipes.database import get_session


class RecipesService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get_all_recipes(
            self, user: User,
            title: str | None,
            dish_type: DishType | None,
            author_id: int | None,
    ) -> list[Recipe]:

        check_user_status(user)
        query = await self.get_filtered_query(title, dish_type, author_id)
        recipes = await self.session.execute(query)
        return recipes.scalars().all()

    async def get_my_recipes(self, user: User) -> list[Recipe]:
        check_user_status(user)
        query = select(Recipe) \
            .where(Recipe.is_active, Recipe.author_id == user.id)
        recipes = await self.session.execute(query)
        return recipes.scalars().all()

    async def get_recipe(self, user: User, id: int) -> Recipe:
        check_user_status(user)
        query = select(Recipe)\
            .where(Recipe.is_active, Recipe.id == id)
        recipe = await self.session.execute(query)
        result = recipe.scalar()
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

    async def change_recipe(self, user: User, id: int, recipe: dict):
        pass

    @classmethod
    async def get_filtered_query(
            cls,
            title: str | None,
            dish_type: DishType | None,
            author_id: int | None
    ):
        query = select(Recipe).where(Recipe.is_active)
        if title is not None:
            query = query.filter(Recipe.title.like(f'%{title}%'))
        if dish_type is not None:
            query = query.filter_by(dish_type=dish_type)
        if author_id is not None:
            query = query.filter_by(author_id=author_id)
        return query.order_by(Recipe.created_at.desc(), Recipe.likes.desc(), Recipe.title)
