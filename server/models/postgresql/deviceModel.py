from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from server.core.database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    device_name = Column(String(255), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    device_type_id = Column(Integer, ForeignKey("device_type.id"), index=True)


    user = relationship("User", back_populates="devices")
    device_type = relationship("DeviceType", back_populates="devices")
    user_gestures =relationship("UserGesture", back_populates="device", cascade="all, delete-orphan")