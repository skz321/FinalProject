from sqlalchemy import Column, Integer, String, Float
from ..dependencies.database import Base
from sqlalchemy.orm import relationship

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    calories = Column(Float, nullable=True)
    category = Column(String(50), nullable=False)

    reviews = relationship("Review", back_populates="menu_item")