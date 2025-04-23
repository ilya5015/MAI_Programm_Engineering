from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    user_id: int = Field(..., examples=[1])
    price: int = Field(..., examples=[1])
    subject: str = Field(..., examples=["Make programm engineering lab work"])
    body: str = Field(..., examples=["Requirements here:"])


class OrderRead(BaseModel):
    user_id: int
    price: int
    subject: str
    body: str
    created_at: datetime

    class Config:
        from_attributes = True

class OrderUpdate(BaseModel):
    price: Optional[bool] = Field(default=None, example=345)
