from fastapi import APIRouter
from .users import router as users_router
from .recipes import router as recipes_router

router = APIRouter()
router.include_router(users_router)
router.include_router(recipes_router)
