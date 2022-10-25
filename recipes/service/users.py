from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.sql.functions import coalesce

from recipes.models.users import UserWithRecipes
from recipes.service.auth import check_user_status
from recipes.service.exceptions import is_blocked_exception
from recipes.tables import User, Recipe
from recipes.database import get_session
from recipes.models import users


class UsersService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get_list(self, user: users.User) -> list[User]:
        """ Получение первых 10 пользователей (кроме заблокированных) """
        check_user_status(user)
        query = select(User) \
            .options(selectinload(User.recipes)) \
            .where(User.is_active)\
            .limit(10)
        result = await self.session.execute(query)
        users = result.scalars().all()
        for i_user in users:
            i_user.recipes_count = len(i_user.recipes)
        users.sort(key=lambda x: x.recipes_count)
        return users

    async def get_profile(self, user: users.User) -> UserWithRecipes:
        query = select(User)\
            .select_from(Recipe)\
            .options(selectinload(User.recipes))\
            .where(User.is_active, User.id == user.id)
        result = await self.session.execute(query)
        user = result.scalar()
        user.recipes_count = len(user.recipes)
        return user
