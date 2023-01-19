"""
Module to configure the project-level logger.
Provides logging functions.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Optional

from .logger import LOGGER, critical, debug, error, info, warning


def configure_logger(
    *,
    level: Optional[int] = None,
    logs_path: Optional[Path] = None,
    debug: bool = __debug__,
) -> None:

    """
    If `level` parameter is left out the level will be
    determined using the __debug__ constant.
    If the `debug` parameter is set to True an additional
    StreamHandler will log everything to sys.stdout.
    Defaults to __debug__.
    """
    if not logs_path and not debug:
        raise ValueError("No file path for regular handler given\
                         and debug handler disabled")

    if not level:
        level = logging.DEBUG if __debug__ else logging.WARNING

    fmt_str = "[%(asctime)s] [%(levelname)s] %(message)s"
    datefmt_str = "%Y-%m-%d %H:%M:%S"

    if logs_path:
        main_handler = logging.FileHandler(logs_path / "latest.log")
        main_handler.setLevel(level)
        main_formatter = logging.Formatter(fmt=fmt_str, datefmt=datefmt_str)
        main_handler.setFormatter(main_formatter)
        LOGGER.addHandler(main_handler)

    if debug:
        debug_handler = logging.StreamHandler(stream=sys.stdout)
        debug_handler.setLevel(logging.DEBUG)
        debug_formatter = logging.Formatter(fmt=fmt_str, datefmt=datefmt_str)
        debug_handler.setFormatter(debug_formatter)
        LOGGER.addHandler(debug_handler)


__all__ = [
    "LOGGER",
    "critical",
    "debug",
    "error",
    "info",
    "warning",
]
