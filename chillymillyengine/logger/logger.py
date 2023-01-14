import logging

LOGGER = logging.getLogger("chilly-milly-logger")


def debug(msg: str, *args, exc_info=None, **kwargs) -> None:
    return LOGGER.debug(msg, *args, exc_info=exc_info, **kwargs)


def info(msg: str, *args, exc_info=None, **kwargs) -> None:
    return LOGGER.info(msg, *args, exc_info=exc_info, **kwargs)


def warning(msg: str, *args, exc_info=None, **kwargs) -> None:
    return LOGGER.warning(msg, *args, exc_info=exc_info, **kwargs)


def error(msg: str, *args, exc_info=None, **kwargs) -> None:
    return LOGGER.error(msg, *args, exc_info=exc_info, **kwargs)


def critical(msg: str, *args, exc_info=None, **kwargs) -> None:
    return LOGGER.critical(msg, *args, exc_info=exc_info, **kwargs)
