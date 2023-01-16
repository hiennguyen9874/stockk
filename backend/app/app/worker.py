import logging
from pathlib import Path

import sentry_sdk
from celery.signals import setup_logging
from sentry_sdk.integrations.celery import CeleryIntegration

from app.core.celery_app import create_celery_app
from app.core.settings import settings
from app.custom_logging import CustomizeLogger

sentry_sdk.init(settings.SENTRY_DSN, integrations=[CeleryIntegration()])


@setup_logging.connect()
def config_loggers(*args, **kwargs) -> logging.Logger:  # type: ignore
    return CustomizeLogger.make_logger(Path(__file__).with_name("celery_logging.json"))


app = create_celery_app()
