from pydantic import BaseModel
from datetime import datetime

class PromotionCodeBase(BaseModel):
    code: str
    expiration_date: datetime

class PromotionCodeCreate(PromotionCodeBase):
    pass

class PromotionCode(PromotionCodeBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True 