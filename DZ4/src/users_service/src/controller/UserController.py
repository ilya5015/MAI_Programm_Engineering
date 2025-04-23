from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..tools.auth import get_password_hash
from ..models.models import User


class UserController:
    @staticmethod
    async def create_user(
        session: AsyncSession,
        login: str,
        password: str,
        name: str,
    ) -> User:
        result = await session.execute(select(User).where(User.login == login))
        if result.scalar_one_or_none():
            raise ValueError("User with this login already exists")

        user = User(
            login=login,
            name=name,
            hashed_password=get_password_hash(password),
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def get_by_login(session: AsyncSession, login: str) -> Optional[User]:
        result = await session.execute(select(User).where(User.login == login))
        return result.scalar_one_or_none()

    @staticmethod
    async def find_by_name(session: AsyncSession, name: str) -> List[User]:
        stmt = select(User)

        stmt = stmt.where(User.name == name)

        result = await session.execute(stmt)
        return result.scalars().all()
