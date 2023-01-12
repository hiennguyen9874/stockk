from sqlalchemy import Column, Integer, String

from app.db.base_class import Base

__all__ = ["Industry"]


class Industry(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    enName = Column(String)
