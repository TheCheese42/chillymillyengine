"""
Contains a wrapper around the Window class from the arcade library.
"""

from typing import Optional

import arcade
import pyglet


class Window(arcade.Window):
    """
    Wrapper around `arcade.Window`. Will eventually provide helper
    methods and extra attributes.
    """
    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        title: Optional[str] = "Window",
        fullscreen: bool = False,
        resizable: bool = False,
        update_rate: float = 1 / 60,
        antialiasing: bool = True,
        gl_version: tuple[int, int] = (3, 3),
        screen: Optional[pyglet.display.Screen] = None,
        style: Optional[str] = pyglet.window.Window.WINDOW_STYLE_DEFAULT,
        visible: bool = True,
        vsync: bool = False,
        gc_mode: str = "context_gc",
        center_window: bool = False,
        samples: int = 4,
        enable_polling: bool = True,
        gl_api: str = "gl",
        draw_rate: float = 1 / 60,
    ) -> None:
        super().__init__(
            width=width,
            height=height,
            title=title,
            fullscreen=fullscreen,
            resizable=resizable,
            update_rate=update_rate,
            antialiasing=antialiasing,
            gl_version=gl_version,
            screen=screen,
            style=style,
            visible=visible,
            vsync=vsync,
            gc_mode=gc_mode,
            center_window=center_window,
            samples=samples,
            enable_polling=enable_polling,
            gl_api=gl_api,
            draw_rate=draw_rate,
        )

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        if not self.fullscreen:
            # Some window managers will not respect minimum size
            if width < self._minimum_size[0]:
                self.width = self._minimum_size[0]
            if height < self._minimum_size[1]:
                self.height = self._minimum_size[1]
