import pytest

from cme.gui import UIFixedSizeLabel
from cme.utils import get_optimal_font_size


@pytest.fixture
def sample_fixedlabel() -> UIFixedSizeLabel:
    return UIFixedSizeLabel(text="Hello World")


@pytest.mark.requires_window
def test_fit_content_blocked(sample_fixedlabel: UIFixedSizeLabel) -> None:
    with pytest.raises(AttributeError):
        sample_fixedlabel.fit_content()


@pytest.mark.requires_window
def test_update_text_size(sample_fixedlabel: UIFixedSizeLabel) -> None:
    optimal_font_size = get_optimal_font_size(
        sample_fixedlabel.text,
        sample_fixedlabel.label.font_name,
        sample_fixedlabel.width,
        sample_fixedlabel.height,
    )
    sample_fixedlabel.update_text_size()
    assert sample_fixedlabel.label.font_size == optimal_font_size
