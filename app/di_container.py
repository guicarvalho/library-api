from functools import lru_cache
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.settings import Settings


@lru_cache
def get_settings():
    return Settings()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    from app.database import AsyncSessionLocal

    async with AsyncSessionLocal() as session:
        yield session
