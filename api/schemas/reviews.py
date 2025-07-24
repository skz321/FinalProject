from pydantic import BaseModel, Field
from typing import Optional

class ReviewBase(BaseModel):
    rating: float = Field(..., ge=1.0, le=5.0)
    review_text: Optional[str] = None
    customer_id: int
    menu_item_id: int

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int

    class ConfigDict:
        from_attributes = True