from sqlalchemy import Column, Integer, String, DECIMAL, DATETIME
from ..dependencies.database import Base
from datetime import datetime


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(300))
    quantity = Column(Integer, nullable=False, default=0)
    unit = Column(String(20), nullable=False)
    cost_per_unit = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DATETIME, default=datetime.utcnow)
    updated_at = Column(DATETIME, default=datetime.utcnow, onupdate=datetime.utcnow)
