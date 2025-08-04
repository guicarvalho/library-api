from collections.abc import Callable
from typing import Any, TypeVar

from pydantic import BaseModel, Field
from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

EntityType = TypeVar("EntityType")


class PageParams(BaseModel):
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size


class Metadata(BaseModel):
    total: int
    page: int
    size: int


class Page[EntityType](BaseModel):
    data: list[EntityType]
    meta: Metadata


async def paginate_query(
    db: AsyncSession,
    adapter: Callable[[Any], EntityType],
    params: PageParams,
    base_query: Select,
) -> Page[EntityType]:
    total_query = select(func.count()).select_from(base_query.subquery())
    total = await db.scalar(total_query)
    result = await db.execute(
        base_query.offset(params.offset).limit(params.size)
    )
    return Page[EntityType](
        data=[adapter(item) for item in result.scalars().all()],
        meta=Metadata(total=total or 0, page=params.page, size=params.size),
    )
