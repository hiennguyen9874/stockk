from typing import (
    Any,
    AsyncIterator,
    Dict,
    Generic,
    Iterator,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import Select

from app.crud.base import CRUDBase
from app.models.ticker import Ticker
from app.schemas.ticker import TickerCreate, TickerUpdate, TickerType, TickerExchange


class CRUDTicker(CRUDBase[Ticker, TickerCreate, TickerUpdate]):
    async def get_by_ticker(self, db: AsyncSession, ticker: str) -> Optional[Ticker]:
        q = await db.execute(select(self.model).where(self.model.ticker == ticker))
        return q.scalars().one_or_none()

    async def search_by_ticker(
        self,
        db: AsyncSession,
        ticker: str,
        limit: int,
        type: Optional[TickerType] = None,
        exchange: Optional[TickerExchange] = None,
    ) -> AsyncIterator[Ticker]:
        query = select(self.model).where(self.model.ticker.like(f"{ticker}%"))
        if type is not None:
            query = query.where(self.model.type == type.value)
        if exchange is not None:
            query = query.where(self.model.exchange == exchange.value)
        query = query.limit(limit).order_by(self.model.ticker)
        q = await db.execute(query)
        return q.scalars().all()


ticker = CRUDTicker(Ticker)
