"""اتصال واقعی به Postgres (SQLAlchemy async)."""
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(settings.DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def init_db() -> None:
    import app.models  # noqa: F401  -- اطمینان از ثبت همهٔ مدل‌ها روی Base قبل از create_all

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
