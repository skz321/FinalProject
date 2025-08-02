from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class MenuItemIngredient(Base):
    __tablename__ = "menu_item_ingredients"

    id = Column(Integer, primary_key=True, index=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    required_quantity = Column(Float, nullable=False)

    menu_item = relationship("MenuItem", back_populates="ingredient_links")
    ingredient = relationship("Ingredient", back_populates="menu_links")
