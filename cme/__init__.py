"""
The Chilly Milly Engine Python Game Library.
"""

import sys

if sys.version_info[0] < 3 or (
    sys.version_info[0] == 3 and sys.version_info[1] < 7
):
    sys.exit("Chilly Milly Engine requires Python 3.7 or above.")


def init_cme(
    app_name: str,
) -> None:
    from . import config
    config.app_name = app_name


# Exports
from arcade import color  # noqa
from arcade import csscolor  # noqa
from arcade import gl  # noqa
from arcade import key  # noqa

__all__ = [
    "color",
    "csscolor",
    "gl",
    "key",
]
