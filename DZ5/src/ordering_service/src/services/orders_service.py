from typing import Optional, List
from datetime import datetime
from ..controller.order_controller import OrderController
from ..models.models import Order


class OrdersService:
    def __init__(self, controller: OrderController):
        self.controller = controller

    async def create_order(
        self,
        user_id: int,
        price: int,
        subject: str,
        body: str,
    ) -> Order:
        return await self.controller.create_email(
            user_id=user_id,
            price=price,
            subject=subject,
            body=body,
            created_at=datetime.utcnow(),
        )

    async def get_order(self, order_id: str) -> Order | None:
        return await self.controller.get(order_id)

    async def list_orders(self) -> List[Order]:
        return await self.controller.list_orders()

    async def search_orders_by_price(self, price: int) -> List[Order]:
        return await self.controller.find_orders_by_subject(price)

    async def delete_order(self, order_id: str) -> bool:
        ord = await self.controller.get_order_by_id(order_id)
        if not ord:
            return False
        await self.controller.delete_order(order_id)
        return True
