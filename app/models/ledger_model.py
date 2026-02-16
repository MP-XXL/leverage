from sqlalchemy import Column, String, Enum, Integer,DECIMAL, DateTime, ForeignKey, func, Date
from .base import Base
from enums import Type



class Ledger(Base):
    __tablename__ = "ledger"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_account = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    amount = Column(DECIMAL(10, 2), default=0)
    ledger_type = Column(Enum(Type), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
