"""SQLAlchemy Async Engine + Redis 클라이언트."""
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

engine = create_async_engine(settings.sqlalchemy_database_url, echo=(settings.ENV == "local"))
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


def get_redis() -> Redis:
    return Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
