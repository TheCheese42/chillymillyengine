from __future__ import annotations
from .paths import SETTINGS_PATH
from pathlib import Path


class Settings:
    """
    Class for managing settings and serializing them into json files.
    """

    @classmethod
    def from_file(self, file: str | Path) -> Settings:  # type: ignore
        ...  # TODO finish this class with from json etc. and find way to (automatically) call this method. # noqa
