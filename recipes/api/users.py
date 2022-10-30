from fastapi import APIRouter, Depends
from fastapi import status

from recipes.models.users import User, UserCreate, UserWithRecipes
from recipes.service.auth import get_current_user
from recipes.service.users import UsersService


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.get('/', response_model=list[UserWithRecipes])
async def get_users(
        service: UsersService = Depends(),
        user: User = Depends(get_current_user)
):
    """ Получение первых 10 пользователей (кроме заблокированных) """
    return await service.get_list(user)


@router.get('/my_profile', response_model=UserWithRecipes)
async def get_my_profile(
        service: UsersService = Depends(),
        user: User = Depends(get_current_user)
):
    """ Получение профиля текущего пользователя """
    return await service.get_profile(user)


@router.get('/profile/{id}', response_model=UserWithRecipes)
async def get_user_profile(
        id: int,
        service: UsersService = Depends(),
        user: User = Depends(get_current_user)
):
    """ Получение профиля пользователя по id"""
    return await service.get_profile(user, id)


@router.patch('/change_username', status_code=status.HTTP_202_ACCEPTED)
async def change_username(
        new_username: str,
        service: UsersService = Depends(),
        user: User = Depends(get_current_user)
):
    """
    Изменение своего никнейма
    - **new_username**:  Новый никнейм
    """
    return await service.change_username(user, new_username)
