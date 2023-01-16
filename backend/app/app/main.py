from functools import partial
from pathlib import Path

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.api.api_v0.api import api_router as api_router_v0
from app.api.deps import add_swagger_config
from app.core.settings import settings
from app.custom_logging import CustomizeLogger
from app.schemas.response import ErrorResponse, Status, ValidationErrorResponse
from app.signals import *  # noqa

sentry_sdk.init(
    settings.SENTRY_DSN, environment=settings.SENTRY_ENVIRONMENT, traces_sample_rate=1.0
)


async def startup(app: FastAPI) -> None:
    app.state.influxdb_client = InfluxDBClientAsync(
        url=f"http://{settings.INFLUXDB_HOST}:{settings.INFLUXDB_PORT}"
    )
    if not await app.state.influxdb_client.ping():
        raise RuntimeError("Can not connect to influxdb server")


async def shutdown(app: FastAPI) -> None:
    if hasattr(app.state, "influxdb_client"):
        await app.state.influxdb_client.close()


def create_app() -> FastAPI:
    app = FastAPI(
        # root_path=settings.PREFIX,
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.PREFIX}/openapi.json",
        docs_url=f"{settings.PREFIX}/docs",
        redoc_url=f"{settings.PREFIX}/redoc",
        swagger_ui_oauth2_redirect_url=f"{settings.PREFIX}/docs/oauth2-redirect",
    )
    logger = CustomizeLogger.make_logger(Path(__file__).with_name("fastapi_logging.json"))
    app.logger = logger
    return app


app = create_app()

app.add_event_handler(event_type="startup", func=partial(startup, app=app))
app.add_event_handler(event_type="shutdown", func=partial(shutdown, app=app))
app.add_middleware(SentryAsgiMiddleware)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY, https_only=True)
add_swagger_config(app)


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    # Exception
    # Override request validation exceptions
    return JSONResponse(
        content=ValidationErrorResponse(
            status=Status.error, message=exc.errors()
        ).dict(),
        status_code=400,
    )


app.add_exception_handler(RequestValidationError, validation_exception_handler)


# Override the HTTPException error handler
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        content=ErrorResponse(
            status=Status.error,
            message=str(exc.detail),
        ).dict(),
        status_code=exc.status_code,
    )


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_exception_handler(HTTPException, http_exception_handler)

app.include_router(api_router_v0, prefix=f"{settings.PREFIX}{settings.API_V0_STR}")
