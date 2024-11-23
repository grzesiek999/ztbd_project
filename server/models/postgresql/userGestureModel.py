from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from server.core.database import Base
from datetime import datetime, timezone



class UserGesture(Base):
    __tablename__ = "user_gestures"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    gesture_id = Column(Integer, ForeignKey("gestures.id"), index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), index=True)

    user = relationship("User", back_populates="user_gestures")
    gesture = relationship("Gesture", back_populates="user_gestures")
    device = relationship("Device", back_populates="user_gestures")