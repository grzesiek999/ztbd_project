from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from core.postgresql.database import Base
from datetime import datetime, timezone


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255))
    email = Column(String(255), index=True, unique=True)
    password_hash = Column(String(255))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    devices = relationship("Device", back_populates="user", cascade="all, delete-orphan")