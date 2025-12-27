from sqlalchemy import Column, String, Enum, Integer, DateTime, ForeignKey, func, Date
from .base import Base
from enums import Verification



class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"),  unique=True, nullable=False)
    leverage_tag = Column(String(20), nullable=True)
    leverage_balance = Column(Integer, default=0)
    acc_number = Column(Integer, nullable=True)
    acc_balance = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)