from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .food_items import FoodItem


class OrderDetailBase(BaseModel):
    amount: int


class OrderDetailCreate(OrderDetailBase):
    order_id: int
    food_item_id: int

class OrderDetailUpdate(BaseModel):
    order_id: Optional[int] = None
    food_item_id: Optional[int] = None
    amount: Optional[int] = None


class OrderDetail(OrderDetailBase):
    id: int
    order_id: int
    food_item: FoodItem = None

    class ConfigDict:
        from_attributes = True