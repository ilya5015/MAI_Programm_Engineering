from fastapi import APIRouter
from ..controllers.users_controller import user_controller

router = APIRouter(prefix='/users')
router.include_router(user_controller.router)