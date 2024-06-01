import pyglet

pyglet.options['shadow_window'] = False

from typing import Generator  # noqa

import arcade  # noqa
import pytest  # noqa

from cme import init_cme  # noqa


@pytest.fixture(scope="session")
def initialize_window() -> Generator[arcade.Window, None, None]:
    window = arcade.Window()
    yield window
    window.close()  # type: ignore[no-untyped-call]


@pytest.fixture(scope="session", autouse=True)
def initialize_cme() -> None:
    init_cme("Test Suite")
