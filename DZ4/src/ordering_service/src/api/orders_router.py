from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from ..db.schemas import OrderCreate, OrderRead, OrderUpdate
from ..services.orders_service import OrdersService
from ..controller.order_controller import OrderController

router = APIRouter(prefix="/orders", tags=["emails"])

orders_service = OrdersService(OrderController())


@router.post("", response_model=OrderRead)
async def create_email(payload: OrderCreate):
    ord = await orders_service.create_order(
        user_id=payload.user_id,
        price=payload.price,
        subject=payload.subject,
        body=payload.body,
    )
    return ord.dict()


@router.get("", response_model=List[OrderRead])
async def list_orders():
    msgs = await orders_service.list_orders()
    return [m.dict() for m in msgs]


@router.get("/search", response_model=List[OrderRead])
async def search_orders(price: int = Query(..., description="Цена для поиска")):
    results = await orders_service.search_orders_by_price(price)
    if not results:
        raise HTTPException(status_code=404, detail="Заказы с такой ценой не найдены")
    return results


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(order_id: str):
    ord = await orders_service.get_order(order_id)
    if not ord:
        raise HTTPException(status_code=404, detail="Order not found")
    return ord.dict()

@router.delete("/{order_ud}")
async def delete_order(order_id: str):
    success = await orders_service.delete_order(order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"detail": "Order deleted"}
