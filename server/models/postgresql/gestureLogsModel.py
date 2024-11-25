from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from server.core.postgresql.database import Base
from datetime import datetime, timezone



class GestureLogs(Base):
    __tablename__ = 'gestureLogs'

    id = Column(Integer, primary_key=True, index=True)
    device_gesture_id = Column(Integer, ForeignKey('device_gestures.id'), index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    device_gesture = relationship("DeviceGesture", back_populates="gesture_logs")
