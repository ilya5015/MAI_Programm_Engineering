import asyncio
import os
import random

from faker import Faker
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.getenv("MONGODB_URL", "mongodb://mongo_db:27017")
DB_NAME   = os.getenv("MONGODB_DB", "email_db")

NUM_ORDERS = 100

MIN_EXISTING = 10

fake = Faker()

async def init_orders():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    col = db.emails

    count = await col.count_documents({})
    if count > MIN_EXISTING:
        print(f"Уже найдено {count} заказов")
        client.close()
        return

    print(f"Генерация {NUM_ORDERS} заказов...")
    docs = []
    for _ in range(NUM_ORDERS):
        user_id = fake.random_int(min=1, max=50)
        price   = fake.random_int(min=1, max=50000)
        subject      = fake.sentence(nb_words=6)
        body         = "\n\n".join(fake.paragraphs(nb=random.randint(1, 4)))
        created_at   = fake.date_time_between(start_date="-30d", end_date="now")

        docs.append({
            "user_id": user_id,
            "price": price,
            "subject": subject,
            "body": body,
            "created_at": created_at,
        })

    result = await col.insert_many(docs)
    print(f"Вставлено: {len(result.inserted_ids)}")
    client.close()

if __name__ == "__main__":
    asyncio.run(init_orders())
