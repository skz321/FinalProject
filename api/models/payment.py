from sqlalchemy import Column, ForeignKey, Integer, String, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    card_last4 = Column(String(4)) # The last four digits of card
    transaction_status = Column(String(50))  # "Success", "Failed"
    payment_date = Column(DATETIME, default=datetime.now)

    order = relationship("Order", back_populates="payment")
