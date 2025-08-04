# pyright: reportUnusedFunction=false

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import UUID, DateTime, event, func, orm
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from app.di_container import get_settings
from app.entities.book import Book
from app.entities.user import User

settings = get_settings()
engine = create_async_engine(
    settings.postgres_uri,
    echo=settings.sqla_echo,
    pool_size=settings.sqla_pool_size,
    max_overflow=settings.sqla_max_overflow,
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, onupdate=func.now(), server_default=func.now()
    )


@event.listens_for(Session, "do_orm_execute")
def _add_filtering_for(execute_state):
    """Intercept all ORM queries. Add a with_loader_criteria option to all
    of them.

    This option applies to SELECT queries and adds a global WHERE criteria
    (or as appropriate ON CLAUSE criteria for join targets) to all objects
    of a certain class or superclass.
    """
    if (
        not execute_state.is_column_load
        and not execute_state.is_relationship_load
        and not execute_state.execution_options.get("include_deleted", False)
    ):
        execute_state.statement = execute_state.statement.options(
            orm.with_loader_criteria(
                SoftDeleteMixin,
                lambda cls: cls.deleted_at.is_(None),
                include_aliases=True,
            )
        )


class SoftDeleteMixin:
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime)


USERS: list[User] = []
BOOKS: list[Book] = []
