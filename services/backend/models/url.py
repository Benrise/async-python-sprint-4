from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Enum
from sqlalchemy.sql import func

from .base import Base
from .enums import VisibilityEnum


class URL(Base):
    __tablename__ = "url"

    id = Column(Integer, primary_key=True, index=True)
    short_id = Column(String(10), unique=True, nullable=False, index=True)
    original_url = Column(Text, nullable=False)
    is_deleted = Column(Boolean, default=False)
    visibility = Column(Enum(VisibilityEnum), default=VisibilityEnum.public)
    created_at = Column(DateTime, server_default=func.now())