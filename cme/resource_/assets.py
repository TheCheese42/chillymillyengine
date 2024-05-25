from __future__ import annotations

"""
Provides useful classes and functions for assets managing.

The `ASSETS_PATH` constant can be configured using the set_assets_path
function.
"""


from pathlib import Path
from typing import Any, Optional

ASSETS_PATH: Optional["AssetsPath"] = None


class AssetsPath(type(Path())):  # type: ignore
    """
    Provides the find_asset method to recursively retrieve the given asset.

    Subclass or instantiate this to create a hierarchie of assets folders
    (e.g. `ImagesPath`, `SoundsPath`, ...).
    """
    def __new__(cls, *pathsegments: str | Path) -> AssetsPath:
        obj: AssetsPath = super().__new__(cls, *pathsegments)
        obj.get = obj.find_asset
        return obj

    # Avoiding using an __init__ because it doesn't work really well with the
    # pathlib Path system

    def find_asset(
        self,
        asset: str,
        preferences: Optional[list[str]] = None,
    ) -> Path:
        """
        Returns first occurrence of the provided filename.

        `assets` parameter may use glob syntax.
        `preferences` should be a tuple containing preferred extensions.
        Defaults to `.png` and `.svg`. If None, the first match will be picked.
        """
        if preferences is None:
            preferences = [".png", ".svg"]

        for item in self.rglob(asset):
            if not preferences or item.suffix in preferences:
                return Path(item)
        else:
            if preferences:
                # Nothing found matching preferences, trying again without any
                return self.find_asset(asset, preferences=[])

            if "." not in asset:
                # .find_asset("filename") without ext should also be allowed
                return self.find_asset(fr"{asset}.*")

            raise FileNotFoundError(
                f"Could not find an asset with glob `{asset}`"
            )


def set_assets_path(assets_path: Path | str) -> None:
    global ASSETS_PATH
    ASSETS_PATH = AssetsPath(Path(assets_path).resolve())


def get_assets_path() -> Optional[AssetsPath]:
    return ASSETS_PATH
