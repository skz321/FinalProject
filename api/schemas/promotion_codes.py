from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal

class PromotionCodeBase(BaseModel):
    code: str
    discount_percentage: Decimal
    minimum_order_amount: Optional[Decimal] = None
    max_uses: Optional[int] = None
    is_active: bool = True
    expiration_date: datetime

class PromotionCodeCreate(PromotionCodeBase):
    pass

class PromotionCodeUpdate(BaseModel):
    discount_percentage: Optional[Decimal] = None
    minimum_order_amount: Optional[Decimal] = None
    max_uses: Optional[int] = None
    is_active: Optional[bool] = None
    expiration_date: Optional[datetime] = None

class PromotionCode(PromotionCodeBase):
    id: int
    current_uses: int
    created_at: datetime

    class Config:
        from_attributes = True

class PromotionCodeValidation(BaseModel):
    code: str
    order_amount: Decimal

class PromotionCodeValidationResponse(BaseModel):
    is_valid: bool
    discount_amount: Optional[Decimal] = None
    discount_percentage: Optional[Decimal] = None
    message: str 