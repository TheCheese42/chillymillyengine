"""Contains the LOGGER constant and convenience logging functions"""

from typing import Optional, Any
import logging

LOGGER = logging.getLogger("chilly-milly-logger")


def debug(
    msg: str,
    *args: Any,
    exc_info: Optional[bool] = None,
    **kwargs: Any
) -> None:
    """Logs at debug level using the engine-wide `chilly-milly-logger`."""
    if LOGGER.isEnabledFor(logging.DEBUG):  # Performance tweak
        return LOGGER.debug(msg, *args, exc_info=exc_info, **kwargs)


def info(
    msg: str,
    *args: Any,
    exc_info: Optional[bool] = None,
    **kwargs: Any
) -> None:
    """Logs at info level using the engine-wide `chilly-milly-logger`."""
    if LOGGER.isEnabledFor(logging.INFO):  # Performance tweak
        return LOGGER.info(msg, *args, exc_info=exc_info, **kwargs)


def warning(
    msg: str,
    *args: Any,
    exc_info: Optional[bool] = None,
    **kwargs: Any
) -> None:
    """Logs at warning level using the engine-wide `chilly-milly-logger`."""
    return LOGGER.warning(msg, *args, exc_info=exc_info, **kwargs)


def error(
    msg: str,
    *args: Any,
    exc_info: Optional[bool] = None,
    **kwargs: Any
) -> None:
    """Logs at error level using the engine-wide `chilly-milly-logger`."""
    return LOGGER.error(msg, *args, exc_info=exc_info, **kwargs)


def critical(
    msg: str,
    *args: Any,
    exc_info: Optional[bool] = None,
    **kwargs: Any
) -> None:
    """
    Logs at critical or fatal level using the engine-wide
    `chilly-milly-logger`.
    """
    return LOGGER.critical(msg, *args, exc_info=exc_info, **kwargs)
