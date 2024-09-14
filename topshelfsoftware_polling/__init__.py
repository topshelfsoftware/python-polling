import logging
from typing import List, Union

from .polling import logger as polling_logger

PACKAGE_NAME = "topshelfsoftware-polling"


def debug():
    """Set the package Loggers to the DEBUG level."""
    _set_logger_levels(level=logging.DEBUG)
    return


def get_package_loggers() -> List[logging.Logger]:
    """Retrieve a list of the Loggers used in the package."""
    loggers = [polling_logger]
    return loggers


def _set_logger_levels(level: Union[int, str]):
    loggers = get_package_loggers()
    for logger in loggers:
        logger.setLevel(level)
        [handler.setLevel(level) for handler in logger.handlers]
    return
