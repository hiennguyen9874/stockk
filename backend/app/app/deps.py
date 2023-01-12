from contextlib import asynccontextmanager, contextmanager
from typing import AsyncGenerator, Generator

from app.db.session import async_session
from app.db.session import session as sync_session


@contextmanager
def sync_get_db() -> Generator:
    """
    Dependency function that yields db sessions
    """

    with sync_session() as session:
        try:
            yield session
        finally:
            session.commit()


@asynccontextmanager
async def get_db() -> AsyncGenerator:
    """
    Dependency function that yields db sessions
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.commit()
