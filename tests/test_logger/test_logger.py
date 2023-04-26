import logging
import sys
from contextlib import redirect_stdout
from typing import Optional

import pytest

from cme import logger


def test_logger_constant() -> None:
    assert isinstance(logger.LOGGER, logging.Logger)


def test_logger_functions() -> None:
    """
    This test only checks if the logger functions don't raise any exceptions.
    """

    logger.configure_logger(level=logger.DEBUG, debug=True)

    logger.debug("Debug")
    logger.info("Info")
    logger.warning("Warning")
    logger.error("Error")
    logger.critical("Critical")
