from fastapi import APIRouter, Depends
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


@router.get('/current_user', response_model=UserWithRecipes)
async def get_profile(service: UsersService = Depends(), user: User = Depends(get_current_user)):
    return await service.get_profile(user)
