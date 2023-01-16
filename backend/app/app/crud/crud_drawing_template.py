from typing import AsyncIterator, Tuple, Dict, Any, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import exc
from sqlalchemy.orm import defer

from app.crud.base import CRUDBase
from app.models.drawing_template import DrawingTemplate
from app.schemas.drawing_template import DrawingTemplateCreate, DrawingTemplateUpdate


class CRUDDrawingTemplate(CRUDBase[DrawingTemplate, DrawingTemplateCreate, DrawingTemplateUpdate]):
    async def get_or_create_with_owner_name(
        self, db: AsyncSession, ownerSource: str, ownerId: str, name: str, content: str
    ) -> Tuple[DrawingTemplate, bool]:
        study_template = (
            (
                await db.execute(
                    select(self.model).where(
                        self.model.ownerSource == ownerSource,
                        self.model.ownerId == ownerId,
                        self.model.name == name,
                    )
                )
            )
            .scalars()
            .one_or_none()
        )

        if study_template:
            return study_template, False

        try:
            study_template = self.model(
                ownerSource=ownerSource, ownerId=ownerId, name=name, content=json.loads(content)
            )
            db.add(study_template)
            await db.commit()
            await db.refresh(study_template)
            return study_template, False
        except exc.IntegrityError:
            db.rollback()
            study_template = (
                (
                    await db.execute(
                        select(self.model).where(
                            self.model.ownerSource == ownerSource,
                            self.model.ownerId == ownerId,
                            self.model.name == name,
                        )
                    )
                )
                .scalars()
                .one()
            )
            return study_template, False

    async def get_multi_by_owner_tool(
        self, db: AsyncSession, *, ownerSource: str, ownerId: str, tool: str
    ) -> AsyncIterator[DrawingTemplate]:
        statement = (
            select(self.model)
            .where(
                self.model.ownerSource == ownerSource,
                self.model.ownerId == ownerId,
                self.model.tool == tool,
            )
            .options(defer(self.model.content))
        )
        q = await db.execute(statement)
        return q.scalars().all()

    async def get_by_owner_tool_name(
        self, db: AsyncSession, ownerSource: str, ownerId: str, tool: str, name: str
    ) -> Optional[DrawingTemplate]:
        q = await db.execute(
            select(self.model).where(
                self.model.ownerSource == ownerSource,
                self.model.ownerId == ownerId,
                self.model.name == name,
                self.model.tool == tool,
            )
        )
        return q.scalars().one_or_none()


drawing_template = CRUDDrawingTemplate(DrawingTemplate)
