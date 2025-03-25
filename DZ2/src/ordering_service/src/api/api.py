from fastapi import APIRouter
from ..controller.OrderController import OrderController
from typing import List
from ..models.models import Order

router = APIRouter(prefix='/orders')

order_controller = OrderController()


@router.post("/orders/", response_model=Order)
def create_order(order: Order):
    return order_controller.create_order(order, token)

@router.get("/orders/", response_model=List[Order])
def get_orders():
    return order_controller.get_orders(token)