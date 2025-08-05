import decimal
from sqlalchemy import Column, Integer, String, DATETIME, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import Numeric

from .model_loader import index
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    customer_name = Column(String(100))
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    order_type = Column(String(20), nullable=False, server_default="")
    description = Column(String(300))
    tracking_number = Column(String(100))
    total_price = Column(Numeric(10, 2), nullable=False, server_default=str(decimal.Decimal("0.00")))
    is_paid = Column(Boolean, index=True, nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=True)
    card = Column(String(19), nullable=True) # Should show xxxx-xxxx-xxxx-last4

    status = Column(String(50), nullable=False, server_default="Pending") # values will be "Pending", "Shipped", "Delivered", "Cancelled"

    # promotion_code = Column(String(32), nullable=True)
    # discount_amount = Column(Numeric(10, 2), nullable=True)
    # final_price = Column(Numeric(10, 2), nullable=True)

    order_details = relationship("OrderDetail", back_populates="order")
    customer = relationship("User", foreign_keys=[customer_id])
    user = relationship("User", foreign_keys=[user_id])