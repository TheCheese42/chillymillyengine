"""
Provides useful utility functions.
"""


from pyglet.text import Label


def get_optimal_font_size(
    text: str,
    font_name: str,
    container_width: int,
    container_height: int,
    max_size: int = 512,
) -> int:
    """
    Calculates the optimal font size to fit a given text inside a container.
    This uses a binary search algorithm for best performance.
    """
    max_size = max_size
    min_size = 1

    while True:
        label = Label(text, font_name=font_name, font_size=max_size)

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
