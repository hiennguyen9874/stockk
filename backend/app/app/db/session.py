from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings

async_engine = create_async_engine(
    settings.ASYNC_SQLALCHEMY_DATABASE_URI,
    echo=settings.DB_ECHO_LOG,
    pool_pre_ping=True,
    future=True,
)

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=settings.DB_ECHO_LOG,
    pool_pre_ping=True,
    future=True,
)

async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
session = sessionmaker(engine, autocommit=False, autoflush=False)
