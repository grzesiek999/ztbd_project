from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from server.core.database import Base


class Gesture(Base):
    __tablename__ = "gestures"

    id = Column(Integer, primary_key=True, index=True)
    gesture_type = Column(String(255), index=True, unique=True)
    description = Column(Text)

    user_gestures = relationship("UserGesture", back_populates= "gesture", cascade="all, delete-orphan")