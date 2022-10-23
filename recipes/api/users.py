from fastapi import APIRouter, Depends
from recipes.models.users import User, UserCreate
from recipes.service.users import UsersService


router = APIRouter(
    prefix='/users'
)


@router.get('/', response_model=list[User])
async def get_users(service: UsersService = Depends()):
    return await service.get_list()


@router.get('/{user_id}', response_model=User)
async def get_user(user_id: int, service: UsersService = Depends()):
    return await service.get_user(user_id)
