from sqlalchemy import Column, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from ..dependencies.database import Base
from datetime import datetime


class Sandwich(Base):
    __tablename__ = "sandwiches"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(300))
    price = Column(DECIMAL(10, 2), nullable=False)
    category = Column(String(50))
    is_available = Column(Integer, default=1)  # 1 for available, 0 for not available
    created_at = Column(DATETIME, default=datetime.utcnow)
    updated_at = Column(DATETIME, default=datetime.utcnow, onupdate=datetime.utcnow)

    order_details = relationship("OrderDetail", back_populates="sandwich")
