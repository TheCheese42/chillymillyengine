import logging
from pathlib import Path
from tempfile import NamedTemporaryFile

from cme import logger


def test_logger_constant() -> None:
    assert isinstance(logger.LOGGER, logging.Logger)


def test_logger_functions() -> None:
    """
    This test only checks if the logger functions don't raise any exceptions.
    """
    with NamedTemporaryFile("x", encoding="utf-8") as tf:
        logger.configure_logger(logs_path=Path(tf.name), level=logger.DEBUG)

        logger.debug("Debug")
        logger.info("Info")
        logger.warning("Warning")
        logger.error("Error")
        logger.critical("Critical")
