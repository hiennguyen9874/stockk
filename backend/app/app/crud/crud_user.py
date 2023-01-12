from typing import Any, Dict, Optional, Tuple, Union

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        q = await db.execute(select(self.model).where(self.model.email == email))

        return q.scalars().one_or_none()

    async def get_or_create_by_email(
        self, db: AsyncSession, email: str, **kwargs: Optional[Any]
    ) -> Tuple[User, bool]:
        user = (
            (await db.execute(select(self.model).where(self.model.email == email)))
            .scalars()
            .one_or_none()
        )
        if user:
            # exist
            return user, False

        try:
            user = self.model(email=email, **kwargs)
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user, True
        except exc.IntegrityError:
            db.rollback()
            user = (
                (await db.execute(select(self.model).where(self.model.email == email)))
                .scalars()
                .one()
            )
            return user, False

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        db_obj = self.model(
            email=obj_in.email,
            full_name=obj_in.full_name,
        )

        db.add(db_obj)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_active(self, user: User) -> bool:
        return user.is_active


user = CRUDUser(User)
