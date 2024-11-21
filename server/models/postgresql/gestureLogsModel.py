from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from server.core.database import Base
from datetime import datetime, timezone



class GestureLogs(Base):
    __tablename__ = 'gesture_logs'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    gesture_id = Column(Integer, ForeignKey("gestures.id"), index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="gesture_logs")
    gesture = relationship("Gesture", back_populates="gesture_logs")
    device = relationship("Device", back_populates="gesture_logs")