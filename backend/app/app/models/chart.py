from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, RelationshipProperty
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base_class import Base
from app.utils import TZDateTime
from sqlalchemy.sql import func

if TYPE_CHECKING:
    from .user import User  # noqa: F401


__all__ = ["Chart"]


class Chart(Base):
    id = Column(Integer, primary_key=True, index=True)
    ownerSource = Column(String, index=True)
    ownerId = Column(String, index=True)
    name = Column(String)
    symbol = Column(String)
    resolution = Column(String)
    lastModified = Column(TZDateTime, onupdate=func.now())
    content = Column(JSONB)
