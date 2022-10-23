from fastapi import APIRouter, Depends
from recipes.models.users import User, UserCreate
from recipes.service.auth import get_current_user
from recipes.service.users import UsersService


router = APIRouter(
    prefix='/users'
)


@router.get('/', response_model=list[User])
async def get_users(
        service: UsersService = Depends(),
        user: User = Depends(get_current_user)
):
    return await service.get_list()


@router.get('/current_user', response_model=User)
async def get_user(user: User = Depends(get_current_user)):
    return user
