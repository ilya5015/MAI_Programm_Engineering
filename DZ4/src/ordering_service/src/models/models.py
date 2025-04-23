from datetime import datetime
from typing import List, Optional


class Order:
    def __init__(
        self,
        order_id: str,
        user_id: int,
        price: int,
        subject: str,
        body: str,
        created_at: datetime,
    ):
        self.order_id = order_id
        self.user_id = user_id
        self.price = price
        self.subject = subject
        self.body = body
        self.created_at = created_at

    def dict(self) -> dict:
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "price": self.price,
            "subject": self.subject,
            "body": self.body,
            "created_at": self.created_at.isoformat(),
        }
