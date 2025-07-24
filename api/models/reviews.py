from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Review(Base):
    __tablename__= "reviews"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Float, nullable=False)
    review_text = Column(String(500), nullable=False)

    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)

    customer = relationship("User", back_populates="reviews")
    menu_item = relationship("MenuItem", back_populates="reviews")

