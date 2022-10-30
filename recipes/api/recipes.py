from fastapi import APIRouter, Depends, status, Body
from fastapi.params import Query
from fastapi_pagination import Page, paginate

from recipes.models.recipes import Recipe, RecipeCreate, RecipeShow, DishType
from recipes.models.users import User
from recipes.service.auth import get_current_user
from recipes.service.recipes import RecipesService

router = APIRouter(
    prefix='/recipes',
    tags=['Recipes']
)


@router.get('/', response_model=Page[Recipe])
async def get_all_recipes(
        title: str | None = Query(default=None),
        dish_type: DishType | None = Query(default=None),
        author_id: int | None = Query(default=None),
        service: RecipesService = Depends(),
        user: User = Depends(get_current_user)
):
    """
    Получение списка рецептов (без поля «шаги приготовления»)
    - **title**: фильтрация по названию/части названия
    - **dish_type**: фильтрация по типу блюда
    - **author_id**: фильтрация по автору (id)
    """

    all_recipes = await service.get_all_recipes(user, title, dish_type, author_id)
    return paginate(all_recipes)


@router.get('/my', response_model=list[Recipe])
async def get_my_recipes(
        service: RecipesService = Depends(),
        user: User = Depends(get_current_user)
):
    """ Получение рецептов текущего пользователя """

    return await service.get_my_recipes(user)


@router.get('/{id}', response_model=RecipeShow)
async def get_recipe(
        id: int,
        service: RecipesService = Depends(),
        user: User = Depends(get_current_user),
):
    """
    Получение конкретного рецепта
    - **id**: id получаемого рецепта
    """

    return await service.get_recipe(user, id)


@router.post('/create', response_model=RecipeCreate, status_code=status.HTTP_201_CREATED)
async def create_recipe(
        operation_data: RecipeCreate,
        service: RecipesService = Depends(),
        user: User = Depends(get_current_user)
):
    """ Добавление пользователем рецепта """

    return await service.create(user, operation_data)
