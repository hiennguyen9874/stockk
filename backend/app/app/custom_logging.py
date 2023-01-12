import json
import logging
import sys
from pathlib import Path
from typing import Dict

from loguru import logger


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: "CRITICAL",
        40: "ERROR",
        30: "WARNING",
        20: "INFO",
        10: "DEBUG",
        0: "NOTSET",
    }

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore
            depth += 1

        # log = logger.bind(request_id="app")
        # log.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class CustomizeLogger:
    @classmethod
    def make_logger(cls, config_path: Path) -> logging.Logger:
        config = cls.load_logging_config(config_path)
        logging_config = config.get("logger")
        return cls.customize_logging(
            logging_config.get("path"),  # type: ignore
            level=logging_config.get("level"),  # type: ignore
            retention=logging_config.get("retention"),  # type: ignore
            rotation=logging_config.get("rotation"),  # type: ignore
            format=logging_config.get("format"),  # type: ignore
        )

    @classmethod
    def customize_logging(
        cls, filepath: Path, level: str, rotation: str, retention: str, format: str
    ) -> logging.Logger:
        logger.remove()
        logger.add(sys.stdout, enqueue=True, backtrace=True, level=level.upper(), format=format)
        logger.add(
            str(filepath),
            rotation=rotation,
            retention=retention,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format,
        )
        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in ["uvicorn", "uvicorn.error", "fastapi", "gunicorn"]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]
        # return logger.bind(request_id=None, method=None)
        return logger

    @classmethod
    def load_logging_config(cls, config_path: Path) -> Dict[str, Dict[str, str]]:
        config = None
        with open(config_path) as config_file:
            config = json.load(config_file)
        return config
