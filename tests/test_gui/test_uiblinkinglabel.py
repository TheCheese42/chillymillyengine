import pyglet
import pytest

from cme.gui import UIBlinkingLabel


@pytest.fixture
def sample_blinkinglabel() -> UIBlinkingLabel:
    return UIBlinkingLabel(text="Hello World")


@pytest.mark.requires_window
def test_property_defaults(
    sample_blinkinglabel: UIBlinkingLabel,
    initialize_window: pyglet.window.Window,
) -> None:
    initialize_window  # to remove not accessed hint
    assert sample_blinkinglabel.blink_speed == 1.0
    assert sample_blinkinglabel.fade_min == 0
    assert sample_blinkinglabel.fade_max == 255
    assert sample_blinkinglabel.do_fade is True


@pytest.mark.requires_window
def test_on_update_down(
    sample_blinkinglabel: UIBlinkingLabel,
    initialize_window: pyglet.window.Window,
) -> None:
    initialize_window  # to remove not accessed hint
    sample_blinkinglabel.on_update(0.5)
    assert sample_blinkinglabel.label.opacity == 128


@pytest.mark.requires_window
def test_on_update_up(
    sample_blinkinglabel: UIBlinkingLabel,
    initialize_window: pyglet.window.Window,
) -> None:
    initialize_window  # to remove not accessed hint
    sample_blinkinglabel.on_update(1)  # Set _opacity to 0
    sample_blinkinglabel.on_update(0.2)
    assert sample_blinkinglabel.label.opacity == 51
