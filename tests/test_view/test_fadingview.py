import pyglet
import pytest

from cme.view import FadingView


@pytest.fixture
def sample_fadingview(initialize_window: pyglet.window.Window) -> FadingView:
    return FadingView(initialize_window, fade_rate=10)


@pytest.mark.requires_window
def test_fade_in(
    sample_fadingview: FadingView,
) -> None:
    sample_fadingview.start_fade_in()
    sample_fadingview.on_update(1)
    assert sample_fadingview._fade_in == 245
    sample_fadingview.on_update(0.2)
    assert sample_fadingview._fade_in == 243
    sample_fadingview.on_update(25)
    assert sample_fadingview._fade_in is None


@pytest.mark.requires_window
def test_fade_out(
    sample_fadingview: FadingView,
) -> None:
    sample_fadingview.start_fade_out()
    sample_fadingview.on_update(1)
    assert sample_fadingview._fade_out == 10
    sample_fadingview.on_update(0.2)
    assert sample_fadingview._fade_out == 12
    sample_fadingview.on_update(25)
    assert sample_fadingview._fade_out == 255
