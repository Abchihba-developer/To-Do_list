from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import settings
from sqlalchemy.orm import DeclarativeBase


async_engine = create_async_engine(
    url=settings.db.DB_URL_ASYNCPG,
    echo=settings.db.echo,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow)


async_session_factory = async_sessionmaker(
    bind=async_engine,
    autocommit=settings.db.autocommit,
    autoflush=settings.db.autoflush,
    expire_on_commit=settings.db.expire_on_commit)


class Base(DeclarativeBase):
    pass
