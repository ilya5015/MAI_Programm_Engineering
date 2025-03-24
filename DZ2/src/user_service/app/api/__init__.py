from fastapi import APIRouter
from .auth_api import router as auth_router
from .user_api import router as user_router

router = APIRouter(
    prefix='/api',
)

router.include_router(auth_router)
router.include_router(user_router)