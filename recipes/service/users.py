from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from recipes.service.auth import check_user_status
from recipes.service.exceptions import is_blocked_exception
from recipes.tables import User
from recipes.database import get_session
from recipes.models import users


class UsersService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get_list(self, user: users.User) -> list[User]:
        """ Получение первых 10 пользователей (кроме заблокированных) """
        check_user_status(user)
        request = select(User)\
            .options(selectinload(User.recipes))\
            .filter_by(is_active=True)\
            .limit(10)
        users = await self.session.execute(request)
        return users.scalars().all()
