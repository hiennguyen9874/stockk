from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base_class import Base

__all__ = ["StudyTemplate"]


class StudyTemplate(Base):
    id = Column(Integer, primary_key=True, index=True)
    ownerSource = Column(String, index=True, nullable=False)
    ownerId = Column(String, index=True, nullable=False)
    name = Column(String, nullable=False)
    content = Column(JSONB, nullable=False)
