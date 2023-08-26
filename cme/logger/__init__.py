"""
Module to configure the project-level logger.
Provides logging functions.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from .logger import LOGGER


def configure_logger(
    *,
    logs_path: Path,
    level: Optional[int] = None,
) -> None:
    """
    Configure the Chilly Milly Logger.

    :param logs_path: A pathlib.Path object pointing to the logs folder.
    :type logs_path: Path
    :param level: The logging level. Get constants from this module, i.e.
    DEBUG, INFO, WARNING, ERROR, CRITICAL. If None it will be either DEBUG or
    WARNING, depending on the __debug__ constant. Defaults to None
    :type level: Optional[int], optional
    """
    if not level:
        level = logging.DEBUG if __debug__ else logging.WARNING

    fmt_str = "[%(asctime)s] [%(levelname)s] %(message)s"
    datefmt_str = "%Y-%m-%d %H:%M:%S"

    (logs_path / "latest.log").unlink(missing_ok=True)
    main_handler = logging.FileHandler(logs_path / "latest.log")
    main_handler.setLevel(level)
    main_formatter = logging.Formatter(fmt=fmt_str, datefmt=datefmt_str)
    main_handler.setFormatter(main_formatter)
    LOGGER.addHandler(main_handler)

    # XXX Stream handler didn't work for some reason. Also it would interfere
    # XXX with the debug console.
    # XXX Low importance log will now also go in the file handler.
    # if debug:
    #     debug_handler = logging.StreamHandler(stream=sys.stdout)
    #     debug_handler.setLevel(logging.DEBUG)
    #     debug_formatter = logging.Formatter(fmt=fmt_str, datefmt=datefmt_str)
    #     debug_handler.setFormatter(debug_formatter)
    #     LOGGER.addHandler(debug_handler)


from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING  # noqa

from .logger import critical, debug, error, info, warning  # noqa

__all__ = [
    "LOGGER",
    "CRITICAL",
    "critical",
    "DEBUG",
    "debug",
    "ERROR",
    "error",
    "INFO",
    "info",
    "WARNING",
    "warning",
]
