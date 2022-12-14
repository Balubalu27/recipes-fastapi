from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from recipes.models.auth import Token
from recipes.models.users import UserCreate
from recipes.service.auth import AuthService

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/sign-up', response_model=Token)
async def sign_up(
        user_data: UserCreate,
        service: AuthService = Depends()
):
    """ Регистрация пользователя """
    return await service.register_new_user(user_data)


@router.post('/sign-in', response_model=Token)
async def sign_in(
        form_data: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends()
):
    """ Авторизация пользователя """

    return await service.authenticate_user(
        form_data.username,
        form_data.password
    )
