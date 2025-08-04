from sqlalchemy.ext.asyncio import AsyncSession

_global_session: AsyncSession | None = None


def set_factory_session(session: AsyncSession) -> None:
    global _global_session
    _global_session = session


def get_factory_session() -> AsyncSession:
    if _global_session is None:
        raise RuntimeError("Factory session has not been set yet.")
    return _global_session
