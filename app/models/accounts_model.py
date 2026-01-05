from sqlalchemy import Column, String, Enum, Integer,DECIMAL, DateTime, ForeignKey, func, Date
from .base import Base
from enums import AccountStatus



class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"),  unique=True, nullable=False)
    leverage_tag = Column(String(20), nullable=True, unique=True)
    leverage_balance = Column(DECIMAL(10, 2), default=0)
    acc_number = Column(Integer, nullable=True)
    acc_balance = Column(DECIMAL(10, 2), default=0)
    acc_status = Column(Enum(AccountStatus), default=AccountStatus.active, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)