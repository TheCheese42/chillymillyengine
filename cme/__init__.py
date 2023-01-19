import sys

import config

if sys.version_info[0] < 3 or (
    sys.version_info[0] == 3 and sys.version_info[1] < 7
):
    sys.exit("Chilly Milly Engine requires Python 3.7 or above.")


def init_cme(
    app_name: str,
):
    config.app_name = app_name


# #flake8: noqa (E402)
