from fastapi import APIRouter, Depends, status

from recipes.models.recipes import Recipe, RecipeCreate
from recipes.models.users import User
from recipes.service.auth import get_current_user
from recipes.service.recipes import RecipesService

router = APIRouter(
    prefix='/recipes'
)


@router.get('/', response_model=list[Recipe])
async def get_recipes(
        service: RecipesService = Depends(),
        user: User = Depends(get_current_user)
):
    return await service.get_list(user.id)


@router.post('/create', response_model=RecipeCreate, status_code=status.HTTP_201_CREATED)
async def create_recipe(
        operation_data: RecipeCreate,
        service: RecipesService = Depends(),
        user: User = Depends(get_current_user)
):
    return await service.create(user.id, operation_data)
