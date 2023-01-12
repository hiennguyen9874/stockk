from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.ticker import Ticker
from app.schemas.ticker import TickerCreate, TickerUpdate


class CRUDTicker(CRUDBase[Ticker, TickerCreate, TickerUpdate]):
    def create_with_industry_id_sync(
        self, db: Session, *, obj_in: TickerCreate, industry_id: str
    ) -> Ticker:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, industry_id=industry_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


ticker = CRUDTicker(Ticker)
