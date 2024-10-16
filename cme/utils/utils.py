"""
Provides useful utility functions.
"""


import math
from collections import defaultdict
from typing import Any, Optional

from arcade.types import Rect
from pyglet.text import Label


def get_optimal_font_size(
    text: str,
    font_name: str,
    container_width: int,
    container_height: int,
    max_size: float = 512,
    multiline: bool = False,
) -> float:
    """
    Calculates the optimal font size to fit a given text inside a container.
    This uses a binary search algorithm for best performance.
    """
    max_size = max_size
    min_size = 1.0

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
        raised when the string is unidentifiable or not. If `True` no exception
        will be raised and the function returns `None`. Defaults to False.

    Raises:
        ValueError: The string is unidentifiable. Only raises when
        `return_false_on_error` is set to `False`.

    Returns:
        bool: The parsed boolean.
    """
    true = ["true", "t", "1", "y", "yes", "enabled", "enable", "on"]
    false = ["false", "f", "0", "n", "no", "disabled", "disable", "off"]
    try:
        if string.lower() in true:
            out = True
        elif string.lower() in false or return_false_on_error:
            out = False
        else:
            raise ValueError(
                f"The value {string} cannot be mapped to boolean."
            )
    except AttributeError:
        if return_false_on_error:
            return False
        raise TypeError(f"The value {string} is not a string.")
    return out


def point_in_rect(x: float, y: float, rect: Rect) -> bool:
    """
    Find out wether the specified point is inside a rectangle.

    :param x: X coordinate of the point
    :type x: float
    :param y: Y coordinate of the point
    :type y: float
    :param rect: Rectangle (See arcade.types.Rect)
    :type rect: Rect
    :return: Wether the point is inside the rectangle
    :rtype: bool
    """
    return (
        rect.left <= x <= rect.left + rect.width
        and rect.bottom <= y <= rect.bottom + rect.height
    )


def missing_keys(dict1: dict[Any, Any], dict2: dict[Any, Any]) -> list[Any]:
    """
    Return all keys available in dict1 but not in dict2.

    :param dict1: The dictionary with all keys
    :type dict1: dict[Any, Any]
    :param dict2: The dictionary possibly missing keys
    :type dict2: dict[Any, Any]
    :return: All keys in dict1 but not in dict2
    :rtype: list[Any]
    """
    missing_keys_list = [key for key in dict1 if key not in dict2]
    return missing_keys_list


def shrink_list_simple(
    input_list: list[Any], output_size: int
) -> list[Any]:
    """
    Reduce a list to a fixed size.
    **THIS ONLY WORKS WHEN len(input_list) % output_size == 0!!!**
    """
    input_list_len = len(input_list)
    every_x_element = input_list_len / output_size
    new_list = []
    x: Optional[int] = None
    for idx, element in enumerate(input_list):
        if x is None:
            x = idx
            new_list.append(element)
            continue
        if idx - x >= every_x_element:
            new_list.append(element)
            x = idx
    return new_list


def even_distributed_downsample(
    original_list: list[Any],
    new_length: int,
    preserve_order: bool = False,
) -> list[Any]:
    """
    Reduce a list to a fixed size while keeping distribution.
    Requires numpy to be installed.

    Args:
        original_list (list[Any]): The list to be shortened.
        new_length (int): The fixed length of the output.
        preserve_order (bool, optional): Wether or not the original order
        should be preserved. If True, no duplicates are allowed. Defaults to
        False.

    Returns:
        list[Any]: The reduced list.
    """
    try:
        import numpy as np
    except ImportError:
        raise ImportError(
            "numpy must be installed for this to work"
        )
    proportions: defaultdict[Any, Any] = defaultdict(int)
    for item in original_list:
        proportions[item] += 1

    categories = list(proportions.keys())
    category_weights = np.array([proportions[cat] for cat in categories])
    category_probs = category_weights / sum(category_weights)

    sampled_indices = np.random.choice(
        len(categories), new_length, p=category_probs)

    new_list = [categories[index] for index in sampled_indices]
    if preserve_order:
        idx_to_element: dict[int, Any] = {}
        for i in new_list:
            idx = original_list.index(i)
            idx_to_element[idx] = i
        idx_to_element = dict(sorted(idx_to_element.items()))
        new_list = list(idx_to_element.values())
    return new_list


def calc_change_x_y(speed: float, angle: float) -> tuple[float, float]:
    """Calculate the movement into X and Y directions based on projectile
    speed and angle.

    Args:
        speed (float): The total speed (often pixels per second) the object
        should fly at.
        angle (float): The angle the object flies to in degrees.

    Returns:
        tuple[float, float]: X and Y direction speed.
    """
    x = round(speed * math.cos(math.radians(angle)), 10)
    y = round(speed * math.sin(math.radians(angle)), 10)
    return x, y


def calc_angle(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """
    Calculate the angle between two points.

    :param p1: The starting point
    :type p1: tuple[float, float]
    :param p2: The target point
    :type p2: tuple[float, float]
    :return: The angle in degrees
    :rtype: float
    """
    delta_x = p2[0] - p1[0]
    delta_y = p2[1] - p1[1]
    angle_radians = math.atan2(delta_y, delta_x)
    angle_degrees = math.degrees(angle_radians)
    if angle_degrees < 0:
        angle_degrees += 360
    return angle_degrees


def jump_vertical_position(yo: float, vo: float, t: float, a: float) -> float:
    """
    Calculate the jump vertical position from jump time.

    :param yo: Initial vertical position
    :type yo: float
    :param vo: Initial vertical acceleration
    :type vo: float
    :param t: Time in jump
    :type t: float
    :param a: Gravity constant
    :type a: float
    :return: Vertical position
    :rtype: float
    """
    return yo + vo * t + 1 / 2 * a * t ** 2


class NullStream:
    def write(self, *args: Any, **kwargs: Any) -> None:
        pass
