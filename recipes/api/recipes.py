from fastapi import APIRouter, Depends

from recipes.models.recipes import Recipe
from recipes.service.recipes import RecipesService

router = APIRouter(
    prefix='/recipes'
)


@router.get('/', response_model=list[Recipe])
async def get_recipes(service: RecipesService = Depends()):
    return await service.get_list()
