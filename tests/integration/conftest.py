from functools import lru_cache
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from testcontainers.postgres import PostgresContainer

from app.database import Base
from app.di_container import get_settings
from app.settings import Settings
from tests.factories.factory_session_state import set_factory_session

postgres_container = PostgresContainer("postgres:12")
postgres_container.start()


@lru_cache
def get_settings_override() -> Settings:
    return Settings(
        environment="test",
        postgres_host=postgres_container.get_container_host_ip(),
        postgres_port=postgres_container.get_exposed_port(5432),
        postgres_user=postgres_container.username,
        postgres_password=postgres_container.password,
        postgres_db=postgres_container.dbname,
    )


settings = get_settings_override()


@pytest_asyncio.fixture(scope="package", autouse=True)
async def create_db():
    from app.database import engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    postgres_container.stop()


@pytest_asyncio.fixture(scope="package", autouse=True)
async def db_session():
    from app.database import AsyncSessionLocal

    db_session = AsyncSessionLocal()
    set_factory_session(db_session)
    yield db_session


@pytest_asyncio.fixture(autouse=True)
async def clean_db(db_session):
    yield
    await db_session.execute(text("SET session_replication_role = 'replica'"))
    for table in reversed(Base.metadata.sorted_tables):
        await db_session.execute(table.delete())
    await db_session.execute(text("SET session_replication_role = 'origin'"))
    await db_session.commit()


@pytest_asyncio.fixture(scope="package", autouse=True)
async def app() -> AsyncGenerator[FastAPI, None]:
    from app.main import app

    app.dependency_overrides[get_settings] = get_settings_override

    mp = pytest.MonkeyPatch()
    mp.setattr("app.di_container.get_settings", get_settings_override)

    yield app

    app.dependency_overrides.clear()
    mp.undo()


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
