from fastapi import APIRouter, Depends, status
from fastapi.params import Query

from recipes.models.recipes import Recipe, RecipeCreate, RecipeShow, DishType
from recipes.models.users import User
from recipes.service.auth import get_current_user
from recipes.service.recipes import RecipesService

router = APIRouter(
    prefix='/recipes'
)


@router.get('/', response_model=list[Recipe])
async def get_all_recipes(
        title: str | None = Query(default=None),
        dish_type: DishType | None = Query(default=None),
        author_id: int | None = Query(default=None),
        service: RecipesService = Depends(),
        user: User = Depends(get_current_user)
):
    return await service.get_all_recipes(user, title, dish_type, author_id)


@router.get('/my', response_model=list[Recipe])
async def get_my_recipes(
        service: RecipesService = Depends(),
        user: User = Depends(get_current_user)
):
    return await service.get_my_recipes(user)


@router.get('/{id}', response_model=RecipeShow)
async def get_recipe(
        id: int,
        service: RecipesService = Depends(),
        user: User = Depends(get_current_user),
):
    return await service.get_recipe(user, id)


@router.post('/create', response_model=RecipeCreate, status_code=status.HTTP_201_CREATED)
async def create_recipe(
        operation_data: RecipeCreate,
        service: RecipesService = Depends(),
        user: User = Depends(get_current_user)
):
    return await service.create(user, operation_data)
