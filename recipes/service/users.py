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

    async def get_user(self, user_id: int) -> User:
        """ Получения профиля пользователя по id """
        request = select(User).options(selectinload(User.recipes))\
            .filter_by(id=user_id)\
            .group_by(User.id)
        result = await self.session.execute(request)
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return user

    async def create(self, user_data: UserCreate) -> User:
        hashed_pass = get_password_hash(user_data.password)
        user = User(username=user_data.username, password=hashed_pass)
        self.session.add(user)
        await self.session.commit()
        return user


# , func.count().label("recipes_count")



