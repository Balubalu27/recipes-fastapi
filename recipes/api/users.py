from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from recipes.database import async_session
from recipes.models.users import User
from recipes.service.users import UsersService
from recipes.tables import User as user_table

router = APIRouter(
    prefix='/users'
)


@router.get('/', response_model=list[User])
async def get_users(service: UsersService = Depends()):
    return await service.get_list()
