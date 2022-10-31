from fastapi import APIRouter, Depends, status

from recipes.models.users import User
from recipes.service.admin import AdminService
from recipes.service.auth import get_current_user

router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)


@router.patch('/change_recipe_status/{id}', status_code=status.HTTP_202_ACCEPTED)
async def change_recipe_status(
        new_status: bool,
        id: int,
        service: AdminService = Depends(),
        user: User = Depends(get_current_user)
):
    """
    Блокировка/разблокировка рецепта
    - **id**: id рецепта
    - **new_status**: новый статус рецепта
    """

    return await service.change_recipe_status(user, new_status, id)


@router.patch('/change_user_status/{id}', status_code=status.HTTP_202_ACCEPTED)
async def change_user_status(
        new_status: bool,
        id: int,
        service: AdminService = Depends(),
        user: User = Depends(get_current_user)
):
    """
    Блокировка/разблокировка пользователя
    - **id**: id пользователя
    - **new_status**: новый статус пользователя
    """
    return await service.change_user_status(user, new_status, id)
