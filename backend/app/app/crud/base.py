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

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        q = await db.execute(select(self.model).where(self.model.id == id))
        return q.scalars().one_or_none()

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[ModelType]:
        q = await db.execute(select(self.model).where(self.model.email == email))
        return q.scalars().one_or_none()

    async def get_multi(
        self, db: AsyncSession, *, offset: int = 0, limit: int = 100
    ) -> AsyncIterator[ModelType]:
        statement = select(self.model).offset(offset).limit(limit).order_by(self.model.id)
        q = await db.execute(statement)
        return q.scalars().all()

    async def get_count(self, db: AsyncSession, query: Select) -> int:
        """Counting of results returned by the query

        Args:
            db (AsyncSession): AsyncSession
            query (Select): query

        Returns:
            int: Number of results returned by the query
        """
        return await db.scalar(
            select(func.count()).select_from(
                query.with_only_columns(self.model.id).subquery()  # type: ignore
            )
        )

    async def is_exists(self, db: AsyncSession, id: Any) -> bool:
        return (
            await db.execute(
                select(func.count())
                .select_from(
                    select(self.model)
                    .where(self.model.id == id)
                    .with_only_columns(self.model.id)
                    .subquery()
                )
                .exists()
            )
        ).scalar()

    async def get_multi_count(
        self, db: AsyncSession, *, offset: int = 0, limit: int = 100
    ) -> Tuple[AsyncIterator[ModelType], int]:
        items = await self.get_multi(db, offset=offset, limit=limit)
        total = await self.get_count(db, select(self.model))
        return items, total

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> Union[ModelType, None]:
        q = await db.execute(select(self.model).where(self.model.id == id))
        obj = q.scalar_one()
        await db.delete(obj)
        await db.commit()
        return obj

    async def remove_object(self, db: AsyncSession, *, db_obj: ModelType) -> None:
        await db.delete(db_obj)
        await db.commit()

    async def remove_all(self, db: AsyncSession) -> None:
        await db.execute(delete(select(self.model)))
        await db.commit()

    def get_sync(self, db: Session, id: Any) -> Optional[ModelType]:
        q = db.execute(select(self.model).where(self.model.id == id))
        return q.scalars().one_or_none()

    def is_exists_sync(self, db: Session, id: Any) -> bool:
        return db.execute(
            select(func.count())
            .select_from(
                select(self.model)
                .where(self.model.id == id)
                .with_only_columns(self.model.id)
                .subquery()
            )
            .exists()
        ).scalar()

    def get_count_sync(self, db: Session, query: Select) -> int:
        """Counting of results returned by the query

        Args:
            db (AsyncSession): AsyncSession
            query (Select): query

        Returns:
            int: Number of results returned by the query
        """
        return db.scalar(
            select(func.count()).select_from(
                query.with_only_columns(self.model.id).subquery()  # type: ignore
            )
        )

    async def get_all(self, db: AsyncSession) -> AsyncIterator[ModelType]:
        statement = select(self.model).order_by(self.model.id)
        q = await db.execute(statement)
        return q.scalars().all()

    def get_all_sync(self, db: Session) -> Iterator[ModelType]:
        statement = select(self.model).order_by(self.model.id)
        q = db.execute(statement)
        return q.scalars().all()

    def create_sync(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
