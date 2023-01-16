from typing import AsyncIterator, Tuple, Dict, Any, Optional

from sqlalchemy import exc
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import defer

from app.crud.base import CRUDBase
from app.models.study_template import StudyTemplate
from app.schemas.study_template import StudyTemplateCreate, StudyTemplateUpdate


class CRUDStudyTemplate(CRUDBase[StudyTemplate, StudyTemplateCreate, StudyTemplateUpdate]):
    async def get_or_create_with_owner_name(
        self, db: AsyncSession, ownerSource: str, ownerId: str, name: str, content: Dict[Any, Any]
    ) -> Tuple[StudyTemplate, bool]:
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
                ownerSource=ownerSource, ownerId=ownerId, name=name, content=content
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

    async def get_multi_by_owner(
        self, db: AsyncSession, *, ownerSource: str, ownerId: str
    ) -> AsyncIterator[StudyTemplate]:
        statement = (
            select(self.model)
            .where(self.model.ownerSource == ownerSource, self.model.ownerId == ownerId)
            .options(defer(self.model.content))
        )
        q = await db.execute(statement)
        return q.scalars().all()

    async def get_by_owner_name(
        self, db: AsyncSession, ownerSource: str, ownerId: str, name: str
    ) -> Optional[StudyTemplate]:
        q = await db.execute(
            select(self.model).where(
                self.model.ownerSource == ownerSource,
                self.model.ownerId == ownerId,
                self.model.name == name,
            )
        )
        return q.scalars().one_or_none()


study_template = CRUDStudyTemplate(StudyTemplate)
