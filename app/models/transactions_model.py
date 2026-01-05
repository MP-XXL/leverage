from sqlalchemy import Column, String, Enum, Integer,DECIMAL, DateTime, ForeignKey, func, Date
from .base import Base
from enums import TransactionType



class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    sender_acc_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    amount = Column(DECIMAL(10, 2), default=0)
    receiver_acc_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    description = Column(String(256), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
