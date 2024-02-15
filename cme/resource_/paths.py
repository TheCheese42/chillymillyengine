"""
Holds several path constants.
"""


from pathlib import Path

from pyglet import resource

from ..config import app_name

# Appdata and settings path
DATA_PATH = Path(resource.get_data_path(app_name))
print(DATA_PATH)
DATA_PATH.mkdir(exist_ok=True)
SETTINGS_PATH = Path(resource.get_settings_path(app_name))
print(SETTINGS_PATH)
SETTINGS_PATH.mkdir(exist_ok=True)

# Logs
LOGS_PATH = DATA_PATH / "logs"
LOGS_PATH.mkdir(exist_ok=True)
