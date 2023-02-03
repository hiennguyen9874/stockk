from enum import Enum
from typing import Optional

from pydantic import BaseModel

__all__ = ["Ticker", "TickerCreate", "TickerUpdate", "TickerType", "TickerExchange"]


class TickerType(str, Enum):
    vn_stock = "vn_stock"
    crypto = "crypto"


class TickerExchange(str, Enum):
    UPCOM = "UPCOM"
    HNX = "HNX"
    HOSE = "HOSE"


class TickerBase(BaseModel):
    ticker: Optional[str] = None
    exchange: Optional[TickerExchange] = None
    name: Optional[str] = None
    full_name: Optional[str] = None
    short_name: Optional[str] = None
    type: Optional[TickerType] = None


# Properties to receive on item creation
class TickerCreate(TickerBase):
    ticker: str
    exchange: Optional[TickerExchange] = None
    name: str
    full_name: str
    short_name: str
    type: TickerType


# Properties to receive on item update
class TickerUpdate(TickerBase):
    pass


# Properties shared by models stored in DB
class TickerInDBBase(TickerBase):
    class Config:
        orm_mode = True

    ticker: str
    exchange: TickerExchange
    name: str
    full_name: str
    short_name: str
    type: TickerType


# Properties to return to client
class Ticker(TickerInDBBase):
    class Config:
        orm_mode = True
