from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from server.core.database import Base


class DeviceType(Base):
    __tablename__ = "deviceTypes"

    id = Column(Integer, primary_key=True, index=True)
    type_name = Column(String(255), index=True, unique=True)

    devices = relationship("Device", back_populates="device_type", cascade="all, delete-orphan")