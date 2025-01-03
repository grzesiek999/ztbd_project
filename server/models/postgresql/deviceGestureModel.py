from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.postgresql.database import Base



class DeviceGesture(Base):
    __tablename__ = "device_gestures"

    device_gesture_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    gesture_id = Column(Integer, ForeignKey("gestures.gesture_id", ondelete="CASCADE"), index=True)
    gesture_name = Column(String)
    device_id = Column(Integer, ForeignKey("devices.device_id", ondelete="CASCADE"), index=True)

    gesture = relationship("Gesture", back_populates="device_gestures")
    device = relationship("Device", back_populates="device_gestures")