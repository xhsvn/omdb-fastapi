import enum
from functools import lru_cache
from typing import Any


from sqlalchemy.engine.url import URL
from pydantic_settings import BaseSettings


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    # jwt config
    jwt_alg: str = "HS256"
    jwt_secret: str = "secret"
    jwt_exp: int = 10  # minutes

    # gcp cloud settings
    google_project_id: str
    pubsub_project_id: str | None = None

    pubsub_movies_fetch_topic: str

    omdb_api_key: str = "apikey"

    # Application settings
    debug: bool = False
    title: str = "Brite Omdb"
    version: str = "0.1.0"

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO

    # Variables for the database
    postgres_host: str | None = None
    postgres_port: int | None = None
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_connection_name: str | None = None
    postgres_echo: bool = False

    @property
    def fastapi_config(self) -> dict[str, Any]:
        return {
            "debug": self.debug,
            "title": self.title,
            "version": self.version,
        }

    @property
    def database_url(self) -> URL:
        if self.postgres_connection_name:
            return URL.create(
                drivername="postgresql+asyncpg",
                username=self.postgres_user,
                password=self.postgres_password,
                database=self.postgres_db,
                query={"host": f"/cloudsql/{self.postgres_connection_name}"},
            )
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
