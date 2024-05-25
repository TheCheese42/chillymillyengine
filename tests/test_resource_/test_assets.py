import tempfile
from pathlib import Path
from typing import Any, Generator

import pytest

from cme import resource_


@pytest.fixture
def temp_assetspath(initialize_cme: None) -> Generator[
    resource_.AssetsPath, None, None
]:
    with tempfile.TemporaryDirectory() as tempdir:
        resource_.set_assets_path(tempdir)
        yield resource_.get_assets_path()  # type: ignore


def test_set_assets_path_constant(
    initialize_cme: None, temp_assetspath: Path
) -> None:
    assets_path = resource_.get_assets_path()
    assert isinstance(assets_path, resource_.AssetsPath)
    assert str(assets_path) == str(temp_assetspath)


def test_assets_path_find_asset(
    initialize_cme: None, temp_assetspath: Path
) -> None:
    (temp_assetspath / "test_asset.png").touch()

    # Full name
    assert temp_assetspath.find_asset(  # type: ignore
        "test_asset.png"
    ).exists()

    # Ext. wildcard
    assert temp_assetspath.find_asset(  # type: ignore
        "test_asset.*"
    ).exists()

    # Name wildcard
    assert temp_assetspath.find_asset(  # type: ignore
        "test_*.png"
    )

    with pytest.raises(FileNotFoundError):
        temp_assetspath.find_asset("unavailable_asset")  # type: ignore
