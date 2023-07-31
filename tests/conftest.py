import pyglet
import pytest

from cme import init_cme


@pytest.mark.requires_window
@pytest.fixture(scope="session")
def initialize_window():# -> pyglet.window.Window:
    window = pyglet.window.Window()
    yield window
    window.close()


@pytest.fixture(scope="session", autouse=True)
def initialize_cme() -> None:
    init_cme("Test Suite")
