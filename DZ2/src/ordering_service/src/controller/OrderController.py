from fastapi import APIRouter, Depends, HTTPException
from ..models.models import Order

fake_orders_db = []

class OrderController:
    def __init__(self):
        self.orders = fake_orders_db

    def create_order(self, order: Order, token: str):
        user = fake_decode_token(token)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        self.orders.append(order)
        return {"msg": "Order created", "order": order}

    def get_orders(self, token: str):
        user = fake_decode_token(token)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        return self.orders

