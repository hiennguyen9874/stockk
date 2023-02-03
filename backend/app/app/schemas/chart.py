from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from app.schemas.response import Status

__all__ = [
    "Chart",
    "ChartCreate",
    "ChartUpdate",
    "ChartGetList",
    "ChartGet",
    "SuccessfulChartCreateResponse",
    "SuccessfulChartUpdateDeleteResponse",
]


class ChartBase(BaseModel):
    ownerSource: Optional[str] = None
    ownerId: Optional[str] = None
    name: Optional[str] = None
    symbol: Optional[str] = None
    resolution: Optional[str] = None
    lastModified: Optional[datetime] = None
    content: Optional[Dict[Any, Any]] = None


# Properties to receive on item creation
class ChartCreate(ChartBase):
    ownerSource: str
    ownerId: str
    name: str
    symbol: str
    resolution: str
    content: Dict[Any, Any]


# Properties to receive on item update
class ChartUpdate(ChartBase):
    pass


# Properties shared by models stored in DB
class ChartInDBBase(ChartBase):
    class Config:
        orm_mode = True

    id: int
    ownerSource: str
    ownerId: str
    name: str
    symbol: str
    resolution: str
    lastModified: datetime
    content: Dict[Any, Any]


# Properties to return to client
class Chart(ChartInDBBase):
    class Config:
        orm_mode = True


class ChartGetList(BaseModel):
    id: int
    name: str
    timestamp: int
    symbol: str
    resolution: str


class ChartGet(BaseModel):
    id: int
    name: str
    timestamp: int
    symbol: str
    resolution: str
    content: Dict[Any, Any]


class SuccessfulChartCreateResponse(BaseModel):
    status: Status = Field(Status.ok)
    id: int


class SuccessfulChartUpdateDeleteResponse(BaseModel):
    status: Status = Field(Status.ok)
