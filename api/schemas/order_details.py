from pydantic import BaseModel
from typing import Optional


class OrderDetailBase(BaseModel):
    menu_item_id: int
    quantity: int
    amount: Optional[float] = None


class OrderDetailCreate(OrderDetailBase):
    order_id: int


class CreateOrderDetailV2(OrderDetailBase):
    pass


class OrderDetailResponseV2(OrderDetailBase):
    id: int
    order_id: int

    class Config:
        from_attributes = True


OrderDetail = OrderDetailResponseV2


class OrderDetailUpdate(OrderDetailBase):
    pass
