from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from typing import List
from ..controller.UserController import UserController
from ..models.models import User

auth_controller = UserController()

router = APIRouter(prefix='/users')

user_controller = UserController()
user_controller.create_admin_user()  

@router.post("/register")
def register(user: User):
    return user_controller.register_user(user)

@router.post("/login")
def login(user: User):
    return user_controller.login_user(user)

@router.get("/verify-token")
def verify_token(token: str):
    return user_controller.verify_token(token)