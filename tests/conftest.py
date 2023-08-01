import pyglet

pyglet.options['shadow_window'] = False

import pytest  # noqa

from cme import init_cme  # noqa


@pytest.mark.requires_window
@pytest.fixture(scope="session")
def initialize_window() -> pyglet.window.Window:
    window = pyglet.window.Window()
    yield window
    window.close()


@pytest.fixture(scope="session", autouse=True)
def initialize_cme() -> None:
    init_cme("Test Suite")
