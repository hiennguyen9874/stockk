from typing import Any, AsyncIterator, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import defer

from app.crud.base import CRUDBase
from app.models.chart import Chart
from app.schemas.chart import ChartCreate, ChartUpdate


class CRUDChart(CRUDBase[Chart, ChartCreate, ChartUpdate]):
    async def get_multi_by_owner(
        self, db: AsyncSession, *, ownerSource: str, ownerId: str
    ) -> AsyncIterator[Chart]:
        statement = (
            select(self.model)
            .where(self.model.ownerSource == ownerSource, self.model.ownerId == ownerId)
            .options(defer(self.model.content))
        )
        q = await db.execute(statement)
        return q.scalars().all()

    async def get_by_id_owner(
        self, db: AsyncSession, id: Any, ownerSource: str, ownerId: str
    ) -> Optional[Chart]:
        q = await db.execute(
            select(self.model).where(
                self.model.id == id,
                self.model.ownerSource == ownerSource,
                self.model.ownerId == ownerId,
            )
        )
        return q.scalars().one_or_none()


chart = CRUDChart(Chart)
