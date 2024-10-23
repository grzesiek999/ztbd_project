
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(255), index=True)
    user_email = Column(String(255), index=True, unique=True)
    password = Column(String(255))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    devices = relationship("Device", back_populates="user")
    user_gestures = relationship("UserGesture", back_populates="user")


class Gesture(Base):
    __tablename__ = "gestures"

    id = Column(Integer, primary_key=True, index=True)
    gesture_name = Column(String(255), index=True)
    description = Column(Text)

    user_gestures = relationship("UserGesture", back_populates= "gesture")


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    device_name = Column(String(255), index=True)
    device_type = Column(String(255), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)

    user = relationship("User", back_populates="devices")
    user_gestures =relationship("UserGesture", back_populates="device")


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