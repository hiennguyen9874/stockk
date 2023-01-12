from __future__ import annotations

from sqlalchemy import Boolean, Column, Integer, String

from app.db.base_class import Base

__all__ = ["User"]


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean(), default=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, index=False, nullable=True)
