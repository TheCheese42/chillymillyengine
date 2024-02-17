"""Exports all arcade text functions and classes."""
from arcade.text import Text, create_text_sprite, draw_text


def center_x(text: Text, width: int) -> None:
    text.x = width / 2 - text.content_width / 2


def center_y(text: Text, height: int) -> None:
    text.y = height / 2 - text.content_height / 2


__all__ = [
    "center_x",
    "center_y",
    "create_text_sprite",
    "draw_text",
    "Text",
]
