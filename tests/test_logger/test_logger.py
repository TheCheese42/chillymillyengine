import atexit
import logging
import os
from pathlib import Path
from tempfile import mkdtemp

from cme import logger


def test_logger_constant() -> None:
    assert isinstance(logger.LOGGER, logging.Logger)


def test_logger_functions() -> None:
    """
    This test only checks if the logger functions don't raise any exceptions.
    """
    tempdir = mkdtemp()

    logger.configure_logger(logs_path=Path(tempdir), level=logger.DEBUG)

    logger.debug("Debug")
    logger.info("Info")
    logger.warning("Warning")
    logger.error("Error")
    logger.critical("Critical")

    atexit.register(lambda: os.unlink(tempdir))
