from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


__all__ = ["DrawingTemplate"]


class DrawingTemplate(Base):
    id = Column(Integer, primary_key=True, index=True)
    ownerSource = Column(String, index=True, nullable=False)
    ownerId = Column(String, index=True, nullable=False)
    name = Column(String, nullable=False)
    tool = Column(String, nullable=False)
    content = Column(JSONB, nullable=False)
