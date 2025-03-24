from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.user import User
from app.dependencies.auth import get_current_client

class UserController:
    def __init__(self):
        self.router = APIRouter(tags=["users"])
        self.router.add_api_route("/users", self.get_users, methods=["GET"], response_model=List[User])
        self.router.add_api_route("/users/{user_id}", self.get_user, methods=["GET"], response_model=User)
        self.router.add_api_route("/users", self.create_user, methods=["POST"], response_model=User)
        self.router.add_api_route("/users/{user_id}", self.update_user, methods=["PUT"], response_model=User)
        self.router.add_api_route("/users/{user_id}", self.delete_user, methods=["DELETE"], response_model=User)
        self.users_db = []

    def get_users(self, current_user: str = Depends(get_current_client)):
        return self.users_db

    def get_user(self, user_id: int, current_user: str = Depends(get_current_client)):
        for user in self.users_db:
            if user.id == user_id:
                return user
        raise HTTPException(status_code=404, detail="User not found")

    def create_user(self, user: User, current_user: str = Depends(get_current_client)):
        for u in self.users_db:
            if u.id == user.id:
                raise HTTPException(status_code=400, detail="User already exists")
        self.users_db.append(user)
        return user

    def update_user(self, user_id: int, updated_user: User, current_user: str = Depends(get_current_client)):
        for index, user in enumerate(self.users_db):
            if user.id == user_id:
                self.users_db[index] = updated_user
                return updated_user
        raise HTTPException(status_code=404, detail="User not found")

    def delete_user(self, user_id: int, current_user: str = Depends(get_current_client)):
        for index, user in enumerate(self.users_db):
            if user.id == user_id:
                deleted_user = self.users_db.pop(index)
                return deleted_user
        raise HTTPException(status_code=404, detail="User not found")

user_controller = UserController()