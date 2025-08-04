from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from typing import List
from .order_details import OrderDetailCreate



class OrderBase(BaseModel):
    user_id: Optional[int] = None
    customer_name: Optional[str] = None
    order_type: Optional[str] = None
    description: Optional[str] = None



class OrderCreate(OrderBase):
    order_details: List[OrderDetailCreate]


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    description: Optional[str] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    tracking_number: Optional[str]
    total_price: float
    status: str
    card: str
    total_price: float
    is_paid: bool = False
    card: str = ""

    class ConfigDict:
        from_attributes = True

class OrderStatus(BaseModel):
    status: str