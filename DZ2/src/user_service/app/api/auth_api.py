from fastapi import APIRouter
from ..controllers.auth_controller import auth_controller

router = APIRouter(prefix='/auth')
router.include_router(auth_controller.router)