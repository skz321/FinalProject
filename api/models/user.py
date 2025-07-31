from sqlalchemy import Column, Integer, String
from ..dependencies.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=True)
    address = Column(String(200), nullable=True)



