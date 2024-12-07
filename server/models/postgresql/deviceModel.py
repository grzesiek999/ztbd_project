from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.postgresql.database import Base


class Device(Base):
    __tablename__ = "devices"

    device_id = Column(Integer, primary_key=True, index=True)
    device_type_id = Column(Integer, ForeignKey("deviceTypes.device_type_id"), index=True)
    device_name = Column(String(255), index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), index=True)


    user = relationship("User", back_populates="devices")
    device_type = relationship("DeviceType", back_populates="devices")
    device_gestures =relationship("DeviceGesture", back_populates="device", cascade="all, delete-orphan")