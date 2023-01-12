from typing import Optional

from pydantic import BaseModel

from app.schemas.industry import Industry, IndustryInDBBase

__all__ = ["Ticker", "TickerCreate", "TickerUpdate"]


class TickerBase(BaseModel):
    ticker: Optional[str] = None
    companyName: Optional[str] = None
    shortName: Optional[str] = None
    exchange: Optional[str] = None


# Properties to receive on item creation
class TickerCreate(TickerBase):
    ticker: str
    companyName: str
    shortName: str
    exchange: str


# Properties to receive on item update
class TickerUpdate(TickerBase):
    pass


# Properties shared by models stored in DB
class TickerInDBBase(TickerBase):
    class Config:
        orm_mode = True

    ticker: str
    companyName: str
    shortName: str
    exchange: str
    industry: IndustryInDBBase


# Properties to return to client
class Ticker(TickerInDBBase):
    class Config:
        orm_mode = True

    industry: Industry
