import logging
import sys
from typing import Optional

from .logger import LOGGER, critical, debug, error, info, warning


def configure_logger(level: Optional[int] = None) -> None:
    """
    If arg `level` is left out the level will be
    determined using the __debug__ constant
    """
    if not level:
        level = logging.DEBUG if __debug__ else logging.WARNING

    debug_handler = logging.StreamHandler(stream=sys.stdout)
    debug_handler.setLevel(logging.DEBUG)
    debug_formatter = logging.Formatter()
    debug_handler.setFormatter(debug_formatter)
    file_handler = logging.FileHandler(LOGS_PATH / "latest.log")

    LOGGER