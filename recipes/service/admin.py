from typing import Union

from fastapi import Depends
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from recipes.database import get_session
from recipes.models.users import User, SuperUser
from recipes.service.auth import check_admin_permission
from recipes.service.exceptions import not_found_exception
from recipes import tables


class AdminService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def change_status(
            self, user: SuperUser,
            table: Union[tables.User, tables.Recipe],
            new_status: bool, id: int
    ):
        check_admin_permission(user)
        query = update(table)\
            .where(table.id == id)\
            .values(is_active=new_status)\
            .returning(table.id)
        result = await self.session.execute(query)
        updated_id = result.scalar()
        if not updated_id:
            raise not_found_exception
        await self.session.commit()
        return {'detail': f'id={id} successfully change status to {new_status}'}

    async def change_recipe_status(self, user: SuperUser, new_status: bool, id: int):
        return await self.change_status(user, tables.Recipe, new_status, id)

    async def change_user_status(self, user: SuperUser, new_status: bool, id: int):
        return await self.change_status(user, tables.User, new_status, id)
