import pytest

from cme import utils


@pytest.mark.requires_window
def test_get_optimal_font_size(initialize_window: None) -> None:
    input_args = [
        ("Hello World!", "Times New Roman", 64, 96),
        ("This is part of our amazing test suite", "Calibri", 12345, 67890),
        ("Sage, the life you give... Have you ever wondered where it's taken from?", "Comic Sans MS", 1000, 200),  # noqa
    ]
    expected_output = [
        9,
        512,
        22,
    ]
    for (
        (text, font_name, container_width, container_height), expected
    ) in zip(input_args, expected_output):
        assert utils.get_optimal_font_size(
            text, font_name, container_width, container_height
        ) == expected
