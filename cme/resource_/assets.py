from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

ASSETS_PATH: Optional["AssetsPath"] = None


class AssetsPath(Path):
    def get_asset(self, asset: str) -> Path:
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


def set_assets_path(assets_path: Path | str) -> None:
    global ASSETS_PATH

    ASSETS_PATH = AssetsPath(Path(assets_path).resolve())
