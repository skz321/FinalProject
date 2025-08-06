from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from .order_details import CreateOrderDetailV2, OrderDetail

# Shared Base Schema
class OrderBase(BaseModel):
    user_id: Optional[int] = None
    customer_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    order_type: Optional[str] = None
    description: Optional[str] = None
    tracking_number: Optional[str] = None
    total_price: Optional[float] = None
    is_paid: Optional[bool] = None
    status: Optional[str] = None
    card: Optional[str] = None

    class Config:
        from_attributes = True


# CREATE
class OrderCreate(OrderBase):
    order_details: List[CreateOrderDetailV2]


# UPDATE
class OrderUpdate(OrderBase):
    order_details: Optional[List[CreateOrderDetailV2]]


# RESPONSE
class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    order_details: List[OrderDetail]

    class Config:
        from_attributes = True


# STATUS ONLY
class OrderStatus(BaseModel):
    status: str
