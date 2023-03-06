"""
Holds several path constants.
"""


from pathlib import Path

from config import app_name
from pyglet import resource

# Appdata and settings path
DATA_PATH = Path(resource.get_data_path(app_name))
DATA_PATH.mkdir(exist_ok=True)
SETTINGS_PATH = Path(resource.get_settings_path(app_name))
SETTINGS_PATH.mkdir(exist_ok=True)

# Logs
LOGS_PATH = DATA_PATH / "logs"
