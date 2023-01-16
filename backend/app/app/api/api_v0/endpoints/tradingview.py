import time
import math
import httpx
from typing import Any, List, Optional

import pandas as pd
import numpy as np
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas, crud
from app.api import deps
from app.schemas.response import Status, SuccessfulResponse

router = APIRouter()


@router.get("/time", response_model=int)
async def get_time() -> Any:
    """
    Get tradingview time
    """
    return int(math.floor(time.time()))


@router.get("/config", response_model=schemas.tradingview.Config, response_model_exclude_none=True)
async def get_config() -> Any:
    """
    Get tradingview config
    """
    return schemas.tradingview.Config(
        exchanges=[
            schemas.tradingview.Exchange(
                name="All Exchanges",
                value="",
                desc="",
            ),
            schemas.tradingview.Exchange(
                name="HOSE",
                value="HOSE",
                desc="Ho Chi Minh Stock Exchange",
            ),
            schemas.tradingview.Exchange(
                name="HNX",
                value="HNX",
                desc="Hanoi Stock Exchange",
            ),
            schemas.tradingview.Exchange(
                name="UPCOM",
                value="UPCOM",
                desc="Unlisted Public Company Market",
            ),
        ],
        supported_resolutions=["1", "5", "15", "30", "60", "D", "W", "M"],
        supports_marks=False,
        supports_time=True,
        supports_timescale_marks=False,
        symbols_types=[
            schemas.tradingview.SymbolType(name="All types", value=""),
            schemas.tradingview.SymbolType(name="Stock", value="stock"),
            schemas.tradingview.SymbolType(name="Index", value="index"),
            schemas.tradingview.SymbolType(name="Crypto", value="crypto"),
        ],
        supports_search=True,
        supports_group_request=False,
    )


@router.get(
    "/symbols",
    response_model=schemas.tradingview.LibrarySymbolInfo,
    response_model_exclude_none=True,
)
async def get_symbols(*, db: AsyncSession = Depends(deps.get_db), symbol: str) -> Any:
    """
    Get tradingview symbols
    """
    ticker = await crud.ticker.get_by_ticker(db=db, ticker=symbol)
    if not ticker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticker not found")
    return schemas.tradingview.LibrarySymbolInfo(
        name=ticker.name,
        full_name=ticker.short_name,
        ticker=ticker.ticker,
        description=ticker.full_name,
        type="stock" if ticker.type == schemas.TickerType.vn_stock else "crypto",
        session="0900-1130,1300-1500" if ticker.type == schemas.TickerType.vn_stock else "24x7",
        exchange=ticker.exchange,
        listed_exchange=ticker.exchange,
        timezone="Asia/Ho_Chi_Minh" if ticker.type == schemas.TickerType.vn_stock else "UTC",
        format=schemas.SeriesFormat.price,
        pricescale=100,
        minmov=1,
        minmove2=0,
        supported_resolutions=["1", "5", "15", "30", "60", "D", "W", "M"],
        has_daily=True,
        has_empty_bars=False,
        has_intraday=True,
        has_no_volume=False,
        has_weekly_and_monthly=True,
        intraday_multipliers=["1", "5", "15", "30", "60"],
    )


@router.get(
    "/search",
    response_model=List[schemas.tradingview.SearchSymbolResultItem],
    response_model_exclude_none=True,
)
async def get_search(
    *,
    db: AsyncSession = Depends(deps.get_db),
    limit: int,
    query: str,
    type: Optional[str] = Query(""),
    exchange: Optional[str] = Query("")
) -> Any:
    """
    Get tradingview search
    """
    tickers = await crud.ticker.search_by_ticker(
        db=db,
        ticker=query,
        limit=limit,
        type=None if (type is None or type == "") else schemas.TickerType[type],
        exchange=None if (exchange is None or exchange == "") else schemas.TickerExchange[exchange],
    )
    return [
        schemas.SearchSymbolResultItem(
            symbol=ticker.ticker,
            full_name=ticker.short_name,
            description=ticker.full_name,
            exchange=ticker.exchange,
            ticker=ticker.ticker,
            type="stock" if ticker.type == schemas.TickerType.vn_stock else "crypto",
        )
        for ticker in tickers
    ]


@router.get(
    "/history", response_model=schemas.tradingview.HistoryResponse, response_model_exclude_none=True
)
async def get_history(
    symbol: str,
    resolution: str,
    from_time: int = Query(..., alias="from"),
    to_time: int = Query(..., alias="to"),
    countback: Optional[int] = Query(None),
) -> Any:
    """
    Get tradingview history
    """

    headers = {
        "Accept": "*/*",
        "Accept-Language": "vi,en;q=0.9",
        "Connection": "keep-alive",
        "Origin": "https://chart.vps.com.vn",
        "Referer": "https://chart.vps.com.vn/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
    }
    params = {
        "resolution": resolution,
        "symbol": symbol,
        "from": str(from_time),
        "to": str(to_time),
    }

    async with httpx.AsyncClient(http2=True) as client:
        response = await client.get(
            "https://histdatafeed.vps.com.vn/tradingview/history",
            params=params,
            headers=headers,
        )
        results = response.json()
        return results


@router.get("/symbol_info")
async def get_symbol_info() -> Any:
    """
    Get tradingview symbol info
    """
    pass


@router.get("/marks")
async def get_marks() -> Any:
    """
    Get tradingview marks
    """
    pass


@router.get("/timescale_marks")
async def get_timescale_marks(
    symbol: str,
    resolution: str,
    from_time: int = Query(..., alias="from"),
    to_time: int = Query(..., alias="to"),
) -> Any:
    """
    Get tradingview timescale_marks
    """
    pass


@router.get("/quotes")
async def get_quotes() -> Any:
    """
    Get tradingview quotes
    """
    pass
