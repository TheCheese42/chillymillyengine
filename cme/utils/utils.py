"""
Provides useful utility functions.
"""


from arcade.types import Rect
from pyglet.text import Label


def get_optimal_font_size(
    text: str,
    font_name: str,
    container_width: int,
    container_height: int,
    max_size: int = 512,
    multiline: bool = False,
) -> int:
    """
    Calculates the optimal font size to fit a given text inside a container.
    This uses a binary search algorithm for best performance.
    """
    max_size = max_size
    min_size = 1

    while True:
        label = Label(
            text,
            font_name=font_name,
            font_size=max_size,
            multiline=multiline,
        )

        if not (
            label.content_width >= container_width or
            label.content_height >= container_height
        ):
            # Break out of the loop as soon as the content fits
            break

        last_max_size = max_size
        max_size //= 2

    try:
        min_size = max_size
        max_size = last_max_size
    except UnboundLocalError:
        return max_size

    while max_size > min_size:
        mid_size = round((max_size + min_size) / 2 + 0.1)
        # +0.1 to make it round up when 0.5+ and down when 0.4-

        label = Label(text, font_name=font_name, font_size=mid_size)

        # check if middle font size fits in container
        if (
            label.content_width <= container_width and
            label.content_height <= container_height
        ):
            # if it does, search in upper half of range
            min_size = mid_size
        else:
            # otherwise, search in lower half of range
            max_size = mid_size - 1

    return min_size


def str2bool(string: str, return_false_on_error: bool = False) -> bool:
    """Parses a string for a boolean value.

    Args:
        string (str): The string to be parsed.
        return_false_on_error (bool, optional): Wether an exception should be
        raised when the string is unidentifyable or not. If `True` no exception
        will be raised and the function returns `None`. Defaults to False.

    Raises:
        ValueError: The string is unidentifyable. Only raises when
        `return_false_on_error` is set to `False`.

    Returns:
        bool: The parsed boolean.
    """
    true = ["true", "t", "1", "y", "yes", "enabled", "enable", "on"]
    false = ["false", "f", "0", "n", "no", "disabled", "disable", "off"]
    if string.lower() in true:
        return True
    elif string.lower() in false or return_false_on_error:
        return False
    else:
        raise ValueError(f"The value {string} cannot be mapped to boolean.")


def point_in_rect(x: int, y: int, rect: Rect) -> bool:
    return (
        rect[0] <= x <= rect[0] + rect[2] and rect[1] <= y <= rect[1] + rect[3]
    )
