from fastapi import APIRouter
from .users import router as users_router
from .recipes import router as recipes_router
from .auth import router as auth_router
from .admin import router as admin_router

router = APIRouter()
router.include_router(users_router)
router.include_router(recipes_router)
router.include_router(auth_router)
router.include_router(admin_router)
