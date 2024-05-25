"""
The Chilly Milly Engine Python Game Library.
"""

import sys

if sys.version_info[0] < 3 or (
    sys.version_info[0] == 3 and sys.version_info[1] < 7
):
    sys.exit("Chilly Milly Engine requires Python 3.7 or above.")


# Check for arcade-accelerate
ACCELERATED = False
try:
    import arcade_accelerate  # noqa
    ACCELERATED = True
except ModuleNotFoundError:
    pass


def init_cme(
    app_name: str,
) -> None:
    from . import config
    config.app_name = app_name

# Exports
from arcade import (check_for_collision, check_for_collision_with_list,  # noqa
                    check_for_collision_with_lists, csscolor, disable_timings,
                    enable_timings, exit, get_display_size, get_fps,
                    get_window, gl, run, tilemap, types)

from . import color, key  # noqa

__all__ = [
    "check_for_collision",
    "check_for_collision_with_list",
    "check_for_collision_with_lists",
    "color",
    "csscolor",
    "disable_timings",
    "enable_timings",
    "exit",
    "get_display_size",
    "get_fps",
    "get_window",
    "gl",
    "key",
    "run",
    "tilemap",
    "types",
]
