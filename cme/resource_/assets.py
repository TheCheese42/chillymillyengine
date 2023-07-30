from __future__ import annotations

"""
Provides useful classes and functions for assets managing.

The `ASSETS_PATH` constant can be configured using the set_assets_path
function.
"""


from pathlib import Path
from typing import Optional

ASSETS_PATH: Optional["AssetsPath"] = None


class AssetsPath(type(Path())):  # type: ignore
    def __new__(cls, *pathsegments: str | Path) -> AssetsPath:
        return super().__new__(cls, *pathsegments)  # type: ignore

    """
    Provides the find_asset method to recursively retrive the given asset.

    Subclass or instantiate this to create a hierarchie of assets folders
    (e.g. `ImagesPath`, `SoundsPath`, ...).
    """

    def find_asset(self, asset: str) -> Path:
        """
        Returns first occurrence of the provided filename.

        `assets` parameter may use glob syntax.
        """

        for item in self.rglob(asset):
            return Path(item)
        else:
            raise FileNotFoundError(
                f"Could not find an asset with glob `{asset}`"
            )

    def get(self, asset: str) -> Path:
        """Alias for find_asset() method."""
        return self.find_asset(asset)


def set_assets_path(assets_path: Path | str) -> None:
    global ASSETS_PATH
    ASSETS_PATH = AssetsPath(Path(assets_path).resolve())


def get_assets_path() -> Optional[AssetsPath]:
    return ASSETS_PATH
