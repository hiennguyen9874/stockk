from typing import Tuple

from sqlalchemy import exc
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.industry import Industry
from app.schemas.industry import IndustryCreate, IndustryUpdate


class CRUDIndustry(CRUDBase[Industry, IndustryCreate, IndustryUpdate]):
    def get_or_create_sync(
        self, db: Session, *, id: int, name: str, enName: str
    ) -> Tuple[Industry, bool]:
        industry = (
            (db.execute(select(self.model).where(self.model.id == id))).scalars().one_or_none()
        )

        if industry:
            # exist
            return industry, False

        try:
            industry = self.model(id=id, name=name, enName=enName)
            db.add(industry)
            db.commit()
            db.refresh(industry)
            return industry, True
        except exc.IntegrityError:
            db.rollback()
            industry = (db.execute(select(self.model).where(self.model.id == id))).scalars().one()
            return industry, False


industry = CRUDIndustry(Industry)
