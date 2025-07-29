from pydantic import BaseModel
from typing import Optional
from .food_items import FoodItem



class RestaurantBase(BaseModel):
    restaurant_name: str
    owner: int


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(BaseModel):
    restaurant_name: Optional[str] = None
    owner: Optional[int] = None


class Restaurant(RestaurantBase):
    id: int
    food_items: list[FoodItem] = []


    class ConfigDict:
        from_attributes = True
