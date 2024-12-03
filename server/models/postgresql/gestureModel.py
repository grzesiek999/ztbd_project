from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from server.core.postgresql.database import Base


class Gesture(Base):
    __tablename__ = "gestures"

    gesture_id = Column(Integer, primary_key=True, index=True)
    gesture_type = Column(String(255), index=True, unique=True)
    description = Column(Text)

    device_gestures = relationship("DeviceGesture", back_populates= "gesture", cascade="all, delete-orphan")