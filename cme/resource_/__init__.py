"""
Module to keep track of paths and manage game saves and settings.
"""

from .assets import ASSETS_PATH, set_assets_path
from .paths import DATA_PATH, LOGS_PATH, SETTINGS_PATH
from .settings import (Settings, load_settings, register_custom_settings_class,
                       save_settings)

__all__ = [
    "ASSETS_PATH",
    "DATA_PATH",
    "load_settings",
    "LOGS_PATH",
    "register_custom_settings_class",
    "save_settings",
    "Settings",
    "SETTINGS_PATH",
    "set_assets_path",
]
