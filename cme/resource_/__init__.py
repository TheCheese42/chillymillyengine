"""
Module to keep track of paths and manage game saves and settings.
"""

from .assets import ASSETS_PATH, set_assets_path
from .paths import DATA_PATH, LOGS_PATH, SETTINGS_PATH

__all__ = [
    "ASSETS_PATH",
    "DATA_PATH",
    "LOGS_PATH",
    "SETTINGS_PATH",
    "set_assets_path",
]
