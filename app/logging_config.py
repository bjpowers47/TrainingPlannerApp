"""Application logging configuration."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.config import APP_NAME, APP_VERSION, ROOT


def configure_logging() -> Path:
    """Write bounded diagnostic logs beside the user's application data."""
    log_directory = ROOT / "logs"
    log_directory.mkdir(parents=True, exist_ok=True)
    log_path = log_directory / "wildcat-training-planner.log"

    handler = RotatingFileHandler(
        log_path,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    )
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    if not any(
        isinstance(existing, RotatingFileHandler)
        and Path(existing.baseFilename) == log_path
        for existing in root_logger.handlers
    ):
        root_logger.addHandler(handler)

    logging.getLogger(__name__).info("Starting %s %s", APP_NAME, APP_VERSION)
    return log_path
