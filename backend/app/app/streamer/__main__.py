from pathlib import Path

import sentry_sdk

from app.core.settings import settings
from app.custom_logging import CustomizeLogger
from app.streamer import app as app_streamer

sentry_sdk.init(settings.SENTRY_DSN)

logger = CustomizeLogger.make_logger(Path(__file__).parent.with_name("streamer_logging.json"))

app_streamer.main()
