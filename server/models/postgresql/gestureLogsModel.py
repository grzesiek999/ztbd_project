from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from core.postgresql.database import Base
from datetime import datetime, timezone



class GestureLogs(Base):
    __tablename__ = 'gestureLogs'

    log_id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))