"""
Module to keep track of paths and manage game saves and settings.
"""

from .assets import ASSETS_PATH, AssetsPath, get_assets_path, set_assets_path
from .paths import DATA_PATH, LOGS_PATH, SETTINGS_PATH
from .settings import (CUSTOM_SETTINGS_CLASS, Settings, load_settings,
                       register_custom_settings_class, save_settings)

__all__ = [
    "AssetsPath",
    "ASSETS_PATH",
    "CUSTOM_SETTINGS_CLASS",
    "DATA_PATH",
    "get_assets_path",
    "get_settings",
    "load_settings",
    "LOGS_PATH",
    "register_custom_settings_class",
    "save_settings",
    "Settings",
    "SETTINGS_PATH",
    "set_assets_path",
]
