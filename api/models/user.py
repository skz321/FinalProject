from sqlalchemy import Column, Integer, String
from ..dependencies.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone_number = Column(String(20), nullable=True)
    address = Column(String(200), nullable=True)

    reviews = relationship("Review", back_populates="customer")


