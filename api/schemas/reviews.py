from pydantic import BaseModel, Field
from typing import Optional

class ReviewBase(BaseModel):
    rating: float = Field(..., ge=1.0, le=5.0)
    review_text: str = Field(..., min_length=1)
    customer_id: int
    menu_item_id: int

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int

    class ConfigDict:
        from_attributes = True

class LowRatedMenuItem(BaseModel):
    id: int
    name: str
    average_rating: float
    review_count: int