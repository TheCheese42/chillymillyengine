"""
Holds several path constants.
"""


from pathlib import Path

from pyglet import resource

try:
    from ..config import app_name
except ImportError:
    import random
    app_name = f"unnamed_cme_game_{random.randint(0, 1_000_000)}"

# Appdata and settings path
DATA_PATH = Path(resource.get_data_path(app_name))
DATA_PATH.mkdir(parents=True, exist_ok=True)
SETTINGS_PATH = Path(resource.get_settings_path(app_name))
SETTINGS_PATH.mkdir(parents=True, exist_ok=True)

# Logs
LOGS_PATH = DATA_PATH / "logs"
LOGS_PATH.mkdir(parents=True, exist_ok=True)
