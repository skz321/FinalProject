from datetime import datetime
from typing import Optional
from pydantic import BaseModel
# from decimal import Decimal
from .order_details import OrderDetail



class OrderBase(BaseModel):
    customer_name: str
    description: Optional[str] = None
    tracking_number: Optional[str] = None
    total_price: Optional[float] = None
    customer_id: Optional[int] = None
    # promotion_code: Optional[str] = None
    # discount_amount: Optional[Decimal] = None
    # final_price: Optional[Decimal] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    description: Optional[str] = None
    tracking_number: Optional[str] = None
    total_price: Optional[float] = None
    customer_id: Optional[int] = None
    # promotion_code: Optional[str] = None
    # discount_amount: Optional[Decimal] = None
    # final_price: Optional[Decimal] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    order_details: list[OrderDetail] = None

    class ConfigDict:
        from_attributes = True
