import asyncio
import os
import sys

from faker import Faker
from sqlalchemy import select, func

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tools.auth import get_password_hash
from db.db import async_session_maker
from models.models import User

fake = Faker()


async def create_dummy_users(count: int = 100):
    async with async_session_maker() as session:
        result = await session.execute(select(func.count()).select_from(User))
        user_count = result.scalar()

        if user_count >= 10:
            return


        for i in range(count):
            name = fake.first_name()
            login = f"user_{i+1}"
            password = get_password_hash("secret")

            user = User(
                name=name,
                login=login,
                hashed_password=password,
            )
            session.add(user)

        await session.commit()


if __name__ == "__main__":
    asyncio.run(create_dummy_users())
