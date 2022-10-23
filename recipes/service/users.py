from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import status

from recipes.models.users import UserCreate
from recipes.tables import User
from recipes.database import get_session


class UsersService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get_list(self) -> list[User]:
        """ Получение первых 10 пользователей (кроме заблокированных) """
        request = select(User)\
            .options(selectinload(User.recipes))\
            .filter(User.is_active)\
            .limit(10)
        users = await self.session.execute(request)
        return users.scalars().all()




