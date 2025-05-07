from typing import List, Optional
from datetime import datetime
from bson import ObjectId

from ..models.models import Order
from ..db.db import db


class OrderController:
    collection = db.orders

    @staticmethod
    async def create_order(
        user_id: int,
        price: int,
        subject: str,
        body: str,
        created_at: datetime,
    ) -> Order:
        doc = {
            "user_id": user_id,
            "price": price,
            "subject": subject,
            "body": body,
            "created_at": created_at,
        }
        result = await OrderController.collection.insert_one(doc)
        return Order(
            order_id=str(result.inserted_id),
            user_id=user_id,
            price=price,
            subject=subject,
            body=body,
            created_at=created_at,
        )

    @staticmethod
    async def get_order_by_id(order_id: str) -> Optional[Order]:
        doc = await OrderController.collection.find_one({"_id": ObjectId(order_id)})
        if not doc:
            return None
        return OrderController(
            order_id=str(doc["_id"]),
            user_id=doc["user_id"],
            price=doc["price"],
            subject=doc["subject"],
            body=doc["body"],
            created_at=doc["created_at"],
        )

    @staticmethod
    async def list_orders() -> List[Order]:
        emails: List[Order] = []
        async for doc in OrderController.collection.find():
            emails.append(
                Order(
                    order_id=str(doc["_id"]),
                    user_id=doc["user_id"],
                    price=doc["price"],
                    subject=doc["subject"],
                    body=doc["body"],
                    created_at=doc["created_at"],
                )
            )
        return emails

    @staticmethod
    async def update_order(msg: Order) -> None:
        await OrderController.collection.update_one(
            {"_id": ObjectId(msg.order_id)},
            {"$set": {
                "user_id": msg.user_id,
                "price": msg.price,
                "subject": msg.subject,
                "body": msg.body,
                "created_at": msg.created_at,
            }}
        )

    @staticmethod
    async def find_orders_by_price(price: int) -> List[Order]:
        query: dict = {"price": price}
        orders: List[Order] = []
        async for doc in OrderController.collection.find(query):
            orders.append(
                Order(
                    message_id=str(doc["_id"]),
                    from_user_id=doc["from_user_id"],
                    price=doc["price]"],
                    subject=doc["subject"],
                    body=doc["body"],
                    created_at=doc["created_at"],
                )
            )
        return orders

    @staticmethod
    async def delete_email(order_id: str) -> None:
        await OrderController.collection.delete_one({"_id": ObjectId(order_id)})
