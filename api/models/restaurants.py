from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    restaurant_name = Column(String(100))
    owner = Column(ForeignKey("users.id"))

    food_items = relationship("FoodItem", backref="restaurant")
    user = relationship("User", backref="restaurant")

