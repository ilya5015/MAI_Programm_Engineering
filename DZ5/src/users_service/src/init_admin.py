import asyncio
import sys
import os

from sqlalchemy import select

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tools.auth import get_password_hash
from db.db import async_session_maker
from models.models import User


async def create_admin():
    async with async_session_maker() as session:
        result = await session.execute(select(User).where(User.login == "admin"))
        user = result.scalar_one_or_none()
        password = get_password_hash("secret")
        print('password is', password)
        if user:
            return

        admin = User(
            name="Admin",
            login="admin",
            hashed_password=password,
        )
        session.add(admin)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(create_admin())
