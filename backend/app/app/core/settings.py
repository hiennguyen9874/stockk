import os
from pathlib import Path
from typing import Any, Dict, Optional

from celery.schedules import crontab
from pydantic import AnyHttpUrl, BaseSettings, HttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
    VERSION: str

    TIME_ZONE: str

    PREFIX: str

    API_V0_STR: str = "/api/v0"

    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

    @property
    def MEDIA_ROOT(self) -> str:
        return os.path.join(self.BASE_DIR, "media")

    MEDIA_URL = "/media/"

    SECRET_KEY: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ALGORITHM: str = "HS256"

    PROJECT_NAME: str

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),  # type: ignore
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    @property
    def ASYNC_SQLALCHEMY_DATABASE_URI(self) -> Optional[str]:
        return (
            self.SQLALCHEMY_DATABASE_URI.replace("postgresql://", "postgresql+asyncpg://")
            if self.SQLALCHEMY_DATABASE_URI
            else self.SQLALCHEMY_DATABASE_URI
        )

    DB_ECHO_LOG: bool = False

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    CELERY_RESULT_SERIALIZER = "json"
    CELERY_TASK_SERIALIZER = "json"
    CELERY_ACCEPT_CONTENT = ["json"]
    CELERY_ENABLE_UTC = True
    CELERY_TIMEZONE: Optional[str] = None

    @validator("CELERY_TIMEZONE")
    def get_celery_timezone(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        return v if isinstance(v, str) else values.get("TIME_ZONE")  # type: ignore

    CELERY_IMPORTS = ("app.tasks",)

    CELERY_BEAT_SCHEDULE: dict = {
        "task-schedule-work": {
            "task": "task_schedule_work",
            "schedule": crontab(minute=1),
        },
        # "task-crawl-ticker": {
        #     "task": "task_crawl_ticker",
        #     "schedule": crontab(minute=1),
        # },
    }

    SENTRY_DSN: Optional[HttpUrl] = None
    SENTRY_ENVIRONMENT: Optional[str] = None

    @validator("SENTRY_DSN", pre=True)
    def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
        return v or None

    OIDC_SERVER: AnyHttpUrl
    OIDC_CLIENT_ID: str
    OIDC_CLIENT_SECRET: str
    OIDC_SCOPES: str

    @property
    def OIDC_DISCOVERY_URL(self) -> str:
        return f"{settings.OIDC_SERVER}/.well-known/openid-configuration"

    INFLUXDB_DB: str
    INFLUXDB_USERNAME: str
    INFLUXDB_PASSWORD: str
    INFLUXDB_HOST: str
    INFLUXDB_PORT: str

    class Config:
        case_sensitive = True


settings = Settings()
