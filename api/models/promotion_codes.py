from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Boolean
from api.dependencies.database import Base
import datetime

class PromotionCode(Base):
    __tablename__ = 'promotion_codes'
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(32), unique=True, index=True, nullable=False)
    discount_percentage = Column(DECIMAL(5, 2), nullable=False, default=0.00)  # e.g., 15.50 for 15.5%
    minimum_order_amount = Column(DECIMAL(10, 2), nullable=True)  # Minimum order amount to apply discount
    max_uses = Column(Integer, nullable=True)  # Maximum number of times this code can be used
    current_uses = Column(Integer, default=0)  # Current number of times used
    is_active = Column(Boolean, default=True)  # Whether the code is active
    expiration_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow) 