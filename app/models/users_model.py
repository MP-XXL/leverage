from sqlalchemy import Column, String, Enum, Integer, DateTime, ForeignKey, func, Date
from .base import Base
from sqlalchemy.orm import relationship
from enums import Verification



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    first_name = Column(String(64), max_length=64, nullable=False)
    last_name = Column(String(64), max_length=64, nullable=False)
    image = Column(String(150), nullable=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(15), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=True)
    address = Column(String(256), nullable=True)
    role = Column(String(10), nullable=True)
    #nationality = Column(Enum(Nationality))
    verification = Column(Enum(Verification), default=Verification.unverified, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("Account", cascade="all, delete", backref="users")