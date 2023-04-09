import pytest
import pyglet
import cme


@pytest.fixture(scope="session")
def initialize_window() -> pyglet.window.Window:
    window = pyglet.window.Window()
    yield window
    window.close()


@pytest.fixture(scope="session", autouse=True)
def initialize_cme() -> None:
    cme.init_cme("Test Suite")
