from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import settings


def normalize_database_url(database_url: str) -> str:
    url = make_url(database_url)
    if url.drivername in ("postgresql", "postgres"):
        return str(url.set(drivername="postgresql+psycopg"))
    return database_url


engine = create_async_engine(normalize_database_url(settings.database_url))

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
