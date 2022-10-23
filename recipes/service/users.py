from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from recipes.tables import User
from recipes.database import get_session


class UsersService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get_list(self) -> list[User]:
        request = select(User).options(selectinload(User.recipes))
        users = await self.session.execute(request)
        return users.scalars().all()
