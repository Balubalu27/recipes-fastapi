from fastapi import APIRouter, Depends
from fastapi import status

from recipes.models.recipes import Recipe
from recipes.models.users import User
from recipes.service.admin import AdminService
from recipes.service.auth import get_current_user
from recipes.service.recipes import RecipesService
from recipes.service.users import UsersService

router = APIRouter(
    prefix='/admin'
)


@router.patch('/change_recipe_status/{id}', status_code=status.HTTP_202_ACCEPTED)
async def change_recipe_status(
        new_status: bool,
        id: int,
        service: AdminService = Depends(),
        user: User = Depends(get_current_user)
):
    return await service.change_recipe_status(user, new_status, id)


@router.patch('/change_user_status/{id}', status_code=status.HTTP_202_ACCEPTED)
async def change_user_status(
        new_status: bool,
        id: int,
        service: AdminService = Depends(),
        user: User = Depends(get_current_user)
):
    return await service.change_user_status(user, new_status, id)
