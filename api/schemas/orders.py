from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from typing import List
from .order_details import OrderDetail
from .order_details import OrderDetailCreate



class OrderBase(BaseModel):
    customer_name: str
    description: Optional[str] = None
    status: str
    tracking_number: Optional[str]
    total_price: float
    order_details: List[OrderDetail]


class OrderCreate(OrderBase):
    customer_name: str
    description: str = ""
    order_details: List[OrderDetailCreate]
    user_id: Optional[int] = None


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    description: Optional[str] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None

    class ConfigDict:
        from_attributes = True

class OrderStatus(BaseModel):
    status: str