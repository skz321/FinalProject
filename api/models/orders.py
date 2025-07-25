import decimal
from sqlalchemy import Column, Integer, String, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import Numeric
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(100))
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    description = Column(String(300))
    status = Column(String(50), nullable=False, server_default="Pending") # values will be "Pending" "Completed"
    tracking_number = Column(String(100))
    total_price = Column(Numeric(10, 2), nullable=False, server_default=str(decimal.Decimal("0.00")))

    order_details = relationship("OrderDetail", back_populates="order")
    payment = relationship("Payment", back_populates="order")