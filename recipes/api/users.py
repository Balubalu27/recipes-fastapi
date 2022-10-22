from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from recipes.database import get_session
from recipes.models.users import User
from recipes.service.users import UsersService

router = APIRouter(
    prefix='/users'
)


@router.get('/', response_model=list[User])
async def get_users(service: UsersService = Depends()):
    return service.get_list()
