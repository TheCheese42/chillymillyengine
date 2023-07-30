"""
Contains a wrapper around the Window class from the arcade library.
"""

from typing import Optional

import arcade


class View(arcade.View):
    def __init__(self, window: Optional[arcade.Window] = None):
        super().__init__(window)


class FadingView(arcade.View):
    """Implements logic to fade a view in and/or out."""
    def __init__(
        self, window: Optional[arcade.Window] = None,
        fade_rate: int = 5,
    ):
        """
        `fade_rate` is the increase/decrease rate of the views opacity per
        second. E.g. with a `fade_rate` of 255 the view takes 1 seconds to
        fade.
        """
        super().__init__(window)
        self.fade_rate = fade_rate
        self._fade_out: Optional[float] = None
        self._fade_in: Optional[float] = None

    def start_fade_in(self):
        """
        Start the fading. Usually called right when the view was constructed
        and set up.
        """
        self._fade_in = 255.0

    def start_fade_out(self):
        """
        Start the fading. Usually called right when the view is about to
        change.
        """
        self._fade_out = 0.0

    def on_update(self, delta_time: float):
        """Overridden to call the update_fade() method."""
        super().on_update(delta_time)
        self.update_fade(delta_time)

    def update_fade(self, delta_time: float):
        """
        Updates the fade while taking into account `the delta_time` value.
        """
        step = self.fade_rate * delta_time

        if self._fade_out is not None:
            self._fade_out += step
            if self._fade_out > 255:
                self._fade_out = 255

        if self._fade_in is not None:
            self._fade_in -= step
            if self._fade_in <= 0:
                self._fade_in = None

    def draw_fading(self):
        if self._fade_out is not None:
            arcade.draw_rectangle_filled(
                center_x=self.window.width / 2,
                center_y=self.window.height / 2,
                width=self.window.width,
                height=self.window.height,
                color=(0, 0, 0, self._fade_out),
            )

        if self._fade_in is not None:
            arcade.draw_rectangle_filled(
                center_x=self.window.width / 2,
                center_y=self.window.height / 2,
                width=self.window.width,
                height=self.window.height,
                color=(0, 0, 0, self._fade_in),
            )
