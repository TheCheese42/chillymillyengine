from typing import Optional

import arcade
import pyglet


class Window(arcade.Window):
    """
    Wrapper around `arcade.Window`. Will eventualle provide helper
    methods and extra attributes
    """
    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        title: Optional[str] = 'Arcade Window',
        fullscreen: bool = False,
        resizable: bool = False,
        update_rate: Optional[float] = 1 / 60,
        antialiasing: bool = True,
        gl_version: tuple[int, int] = (3, 3),
        screen: pyglet.canvas.Screen = None,
        style: Optional[str] = pyglet.window.Window.WINDOW_STYLE_DEFAULT,
        visible: bool = True,
        vsync: bool = False,
        gc_mode: str = "context_gc",
        center_window: bool = False,
        samples: int = 4,
        enable_polling: bool = True,
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
        )
