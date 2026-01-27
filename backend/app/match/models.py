import uuid
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.base import Base

class Match(Base):
    __tablename__ = "matches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    team_a = Column(String, nullable=False)
    team_b = Column(String, nullable=False)
    venue = Column(String, nullable=False)
    status = Column(String, default="LIVE")  # LIVE, COMPLETED
    created_at = Column(DateTime, server_default=func.now())
