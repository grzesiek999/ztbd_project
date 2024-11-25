from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from server.core.postgresql.database import Base
from datetime import datetime, timezone


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(255), index=True)
    user_email = Column(String(255), index=True, unique=True)
    password = Column(String(255))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    devices = relationship("Device", back_populates="user", cascade="all, delete-orphan")