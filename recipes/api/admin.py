from fastapi import APIRouter, Depends
from fastapi import status

from recipes.models.recipes import Recipe
from recipes.models.users import User
from recipes.service.auth import get_current_user
from recipes.service.recipes import RecipesService

router = APIRouter(
    prefix='/admin'
)


@router.patch('/change_recipe_status/{id}', status_code=status.HTTP_202_ACCEPTED)
async def change_recipe_status(
        recipe_status: bool,
        id: int,
        service: RecipesService = Depends(),
        user: User = Depends(get_current_user)
):
    return await service.change_status(user, recipe_status, id)


# @router.patch('/change_user_status', response_model=RecipeCreate, status_code=status.HTTP_201_CREATED)
# async def create_recipe(
#         operation_data: RecipeCreate,
#         service: RecipesService = Depends(),
#         user: User = Depends(get_current_user)
# ):
#     return await service.create(user, operation_data)