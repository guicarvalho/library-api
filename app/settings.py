from typing import Annotated

from pydantic import StringConstraints
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    environment: str = "dev"
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    log_level: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            to_upper=True,
            pattern=r"^(INFO|WARNING|ERROR|DEBUG)",
        ),
    ] = "INFO"

    # SQLAlchemy
    sqla_echo: bool = False
    sqla_pool_size: int = 10
    sqla_max_overflow: int = 20

    # PostegreSQL
    postgres_user: str = ""
    postgres_password: str = ""
    postgres_host: str = ""
    postgres_port: int = 5432
    postgres_db: str = ""

    @property
    def postgres_uri(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
