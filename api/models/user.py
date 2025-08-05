from ..dependencies.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DATETIME
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=True)
    address = Column(String(200), nullable=True)
    order_type_preference = Column(String(20), nullable=True)

    reviews = relationship("Review", back_populates="customer")
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DATETIME, default=datetime.utcnow)
    updated_at = Column(DATETIME, default=datetime.utcnow, onupdate=datetime.utcnow)



