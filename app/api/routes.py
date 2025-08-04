from typing import Annotated

import asyncpg
from fastapi import APIRouter, Depends

from app.di_container import get_settings
from app.settings import Settings

router = APIRouter()


@router.get("/healthz", tags=["infra"])
async def healthcheck(settings: Annotated[Settings, Depends(get_settings)]):
    response = {"postgres": "ok"}
    try:
        conn = await asyncpg.connect(
            user=settings.postgres_user,
            password=settings.postgres_password,
            database=settings.postgres_db,
            host=settings.postgres_host,
            port=settings.postgres_port,
            timeout=15,
            command_timeout=5,
        )
        await conn.fetch("SELECT version()")
        await conn.close()
    except Exception:
        response["postgres"] = "error"
    return response
