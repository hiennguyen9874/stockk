from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, RelationshipProperty
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.utils import TZDateTime

if TYPE_CHECKING:
    from .user import User  # noqa: F401


__all__ = ["Chart"]


class Chart(Base):
    id = Column(Integer, primary_key=True, index=True)
    ownerSource = Column(String, index=True, nullable=False)
    ownerId = Column(String, index=True)
    name = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    resolution = Column(String, nullable=False)
    lastModified = Column(TZDateTime, default=func.now(), onupdate=func.now(), nullable=False)
    content = Column(JSONB, nullable=False)
