from typing import Optional

from pydantic import BaseModel

__all__ = ["Industry", "IndustryCreate", "IndustryUpdate"]


class IndustryBase(BaseModel):
    name: Optional[str] = None
    enName: Optional[str] = None


# Properties to receive on item creation
class IndustryCreate(IndustryBase):
    name: str
    enName: str


# Properties to receive on item update
class IndustryUpdate(IndustryBase):
    pass


# Properties shared by models stored in DB
class IndustryInDBBase(IndustryBase):
    class Config:
        orm_mode = True

    id: int
    name: str
    enName: str


# Properties to return to client
class Industry(IndustryInDBBase):
    class Config:
        orm_mode = True
