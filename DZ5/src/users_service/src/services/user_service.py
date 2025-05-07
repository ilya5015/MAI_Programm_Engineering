from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession

from ..models.models import User
from ..controller.UserController import UserController


class UserService:
    def __init__(self, controller: UserController):
        self.controller = controller

    async def register_user(self, session, login: str, password: str, name: str) -> User:

        existing = await self.controller.get_by_login(session, login)
        if existing:
            raise ValueError(f"Login '{login}' is already taken")
        return await self.controller.create_user(session, login, password, name)

    async def get_user_by_login(self, session, login: str) -> Optional[User]:
        return await self.controller.get_by_login(session, login)

    async def find_users_by_name(self, session, name: str) -> List[User]:
        return await self.controller.find_by_name(session, name)
