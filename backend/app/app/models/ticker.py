from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, RelationshipProperty

from app.db.base_class import Base

if TYPE_CHECKING:
    from .industry import Industry  # noqa: F401

__all__ = ["Ticker"]


class Ticker(Base):
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True, unique=True)
    exchange = Column(String)
    name = Column(String)
    full_name = Column(String)
    short_name = Column(String)
    type = Column(String)
