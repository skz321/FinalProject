from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class OrderDetail(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    amount = Column(Integer, nullable=True)
    quantity = Column(Integer, nullable=True)

    order = relationship("Order", back_populates="order_details", lazy="joined")
    menu_item = relationship("MenuItem", back_populates="order_details")
