from enum import Enum

from typing import List, Optional, Dict, Union
from pydantic import BaseModel


class Exchange(BaseModel):
    name: str
    value: str
    desc: str


class SymbolType(BaseModel):
    name: str
    value: str


class Unit(BaseModel):
    id: str
    name: str
    description: str


class Config(BaseModel):
    exchanges: Optional[List[Exchange]] = None
    supported_resolutions: Optional[List[str]] = None
    units: Optional[Dict[str, List[Unit]]] = None
    currency_codes: Optional[List[str]] = None
    supports_marks: Optional[bool] = None
    supports_time: Optional[bool] = None
    supports_timescale_marks: Optional[bool] = None
    symbols_types: Optional[List[SymbolType]] = None
    supports_search: Optional[bool] = None
    supports_group_request: Optional[bool] = None


class SeriesFormat(str, Enum):
    price = "price"
    volume = "volume"


class DataStatus(str, Enum):
    streaming = "streaming"
    endofday = "endofday"
    pulsed = "pulsed"
    delayed_streaming = "delayed_streaming"


class LibrarySymbolInfo(BaseModel):
    name: str
    full_name: str
    base_name: Optional[List[str]] = None
    ticker: Optional[str] = None
    description: str
    type: str
    session: str
    session_display: Optional[str] = None
    holidays: Optional[str] = None
    corrections: Optional[str] = None
    exchange: str
    listed_exchange: str
    timezone: str  # TODO: Timezone type
    format: SeriesFormat
    pricescale: float
    minmov: int
    fractional: Optional[bool] = None
    minmove2: int
    has_intraday: Optional[bool] = None
    supported_resolutions: List[str]
    intraday_multipliers: Optional[List[str]] = None
    has_seconds: Optional[bool] = None
    has_ticks: Optional[bool] = None
    seconds_multipliers: Optional[List[str]] = None
    has_daily: Optional[bool] = None
    has_weekly_and_monthly: Optional[bool] = None
    has_empty_bars: Optional[bool] = None
    has_no_volume: Optional[bool] = None
    volume_precision: Optional[int] = None
    data_status: Optional[DataStatus] = None
    expired: Optional[bool] = None
    expiration_date: Optional[int] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    currency_code: Optional[str] = None
    original_currency_code: Optional[str] = None
    unit_id: Optional[str] = None
    original_unit_id: Optional[str] = None
    unit_conversion_types: Optional[List[str]] = None


class SearchSymbolResultItem(BaseModel):
    symbol: str
    full_name: str
    description: str
    exchange: str
    ticker: str
    type: str


class HistoryFullDataResponse(BaseModel):
    s: str
    t: List[int]
    c: List[float]
    o: List[float]
    h: List[float]
    l: List[float]
    v: List[int]


class HistoryPartialDataResponse(BaseModel):
    s: str
    t: List[int]
    c: List[float]
    o: Optional[List[float]] = []
    h: Optional[List[float]] = []
    l: Optional[List[float]] = []
    v: Optional[List[int]] = []


class HistoryNoDataResponse(BaseModel):
    s: str
    nextTime: Optional[int] = None


class HistoryErrorResponse(BaseModel):
    s: str
    errmsg: str


class HistoryResponse(BaseModel):
    __root__: Union[
        HistoryFullDataResponse,
        HistoryPartialDataResponse,
        HistoryNoDataResponse,
        HistoryErrorResponse,
    ]


class TimescaleMarkColor(BaseModel):
    red = "red"
    green = "green"
    blue = "blue"
    yellow = "yellow"


class TimescaleMark(BaseModel):
    id: Union[str, int]
    time: int
    color: TimescaleMarkColor
    label: str
    tooltip: List[str]
