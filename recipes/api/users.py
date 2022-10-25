from fastapi import APIRouter, Depends
from fastapi import status

from recipes.models.users import User, UserCreate, UserWithRecipes
from recipes.service.auth import get_current_user
from recipes.service.users import UsersService


router = APIRouter(
    prefix='/users'
)


@router.get('/', response_model=list[UserWithRecipes])
async def get_users(
        service: UsersService = Depends(),
        user: User = Depends(get_current_user)
):
    return await service.get_list(user)


@router.get('/my_profile', response_model=UserWithRecipes)
async def get_profile(service: UsersService = Depends(), user: User = Depends(get_current_user)):
    return await service.get_profile(user)


@router.patch('/change_username', status_code=status.HTTP_202_ACCEPTED)
async def change_user_status(
        new_username: str,
        service: UsersService = Depends(),
        user: User = Depends(get_current_user)
):
    return await service.change_username(user, new_username)
