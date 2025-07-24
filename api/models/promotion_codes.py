from sqlalchemy import Column, Integer, String, DateTime
from api.dependencies.database import Base
import datetime

class PromotionCode(Base):
    __tablename__ = 'promotion_codes'
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(32), unique=True, index=True, nullable=False)
    expiration_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow) 