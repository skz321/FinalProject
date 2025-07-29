from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class FoodItemBase(BaseModel):
    food_item_name: str
    price: float


class FoodItemCreate(FoodItemBase):
    pass


class FoodItemUpdate(BaseModel):
    food_item_name: Optional[str] = None
    price: Optional[float] = None


class FoodItem(FoodItemBase):
    id: int

    class ConfigDict:
        from_attributes = True