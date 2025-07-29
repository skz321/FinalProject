from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .resources import Resource
from .food_items import FoodItem


class RecipeBase(BaseModel):
    amount: int


class RecipeCreate(RecipeBase):
    food_item_id: int
    resource_id: int

class RecipeUpdate(BaseModel):
    food_item_id: Optional[int] = None
    resource_id: Optional[int] = None
    amount: Optional[int] = None

class Recipe(RecipeBase):
    id: int
    food_item: FoodItem = None
    resource: Resource = None

    class ConfigDict:
        from_attributes = True