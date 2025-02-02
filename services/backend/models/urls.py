from datetime import datetime, UTC
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text

from .base import Base

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    short_id = Column(String(10), unique=True, nullable=False, index=True)
    original_url = Column(Text, nullable=False)
    is_deleted = Column(Boolean, default=False)
    visibility = Column(String(10), default="public")
    created_at = Column(DateTime, server_default=datetime.now(tz=UTC))