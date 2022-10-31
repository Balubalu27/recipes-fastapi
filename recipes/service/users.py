from fastapi import Depends
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from recipes.database import get_session
from recipes.models import users
from recipes.service.auth import check_user_status
from recipes.service.exceptions import not_found_exception
from recipes.tables import User


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
        users.sort(key=lambda x: x.recipes_count, reverse=True)
        return users

    async def get_profile(self, user: users.User, id: int | None = None) -> User:
        """ Получения профиля пользователя """

        user_id = user.id
        if id is not None:
            user_id = id
        query = select(User) \
            .options(selectinload(User.recipes))\
            .where(User.is_active, User.id == user_id)
        result = await self.session.execute(query)
        user = result.scalar()
        if not user:
            raise not_found_exception
        user.recipes_count = len(user.recipes)
        return user

    async def change_username(self, user: users.User, username: str):
        """ Изменение своего никнейма """
        query = update(User) \
            .where(User.id == user.id) \
            .values(username=username) \
            .returning(User.id)
        result = await self.session.execute(query)
        updated_id = result.scalar()
        if not updated_id:
            raise not_found_exception
        await self.session.commit()
        return {'detail': f'Successfully change username to {username}'}
