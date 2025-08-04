from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository(ABC):
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    @abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        pass
