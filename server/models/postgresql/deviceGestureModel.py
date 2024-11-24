from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from server.core.database import Base



class DeviceGesture(Base):
    __tablename__ = "device_gestures"

    id = Column(Integer, primary_key=True, index=True)
    gesture_name = Column(String)
    gesture_id = Column(Integer, ForeignKey("gestures.id"), index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), index=True)

    gesture = relationship("Gesture", back_populates="device_gestures")
    device = relationship("Device", back_populates="device_gestures")
    gesture_logs = relationship("GestureLogs", back_populates="device_gesture", cascade="all, delete-orphan")
