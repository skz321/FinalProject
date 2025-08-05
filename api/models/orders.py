from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    customer_name = Column(String(100))
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    description = Column(String(300))
    status = Column(String(50), nullable=False, server_default="Pending") # values will be "Pending", "Shipped", "Delivered", "Cancelled"
    tracking_number = Column(String(64), nullable=True)
    total_price = Column(DECIMAL(10, 2), nullable=True)
    # promotion_code = Column(String(32), nullable=True)
    # discount_amount = Column(DECIMAL(10, 2), nullable=True)
    # final_price = Column(DECIMAL(10, 2), nullable=True)

    order_details = relationship("OrderDetail", back_populates="order")
    customer = relationship("User")