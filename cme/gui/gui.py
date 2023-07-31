"""
Defines custom gui elements.
"""


from typing import Any, Literal, Optional

from arcade import gui, types

from ..utils import get_optimal_font_size


class UIFixedSizeLabel(gui.UILabel):
    def fit_content(self) -> None:
        raise AttributeError(f"Cannot resize {self.__class__.__name__}.")

    def update_text_size(self) -> None:
        """Sets the Text to the maximum possible size for the widget size."""
        optimal_font_size = get_optimal_font_size(
            text=self.text,
            font_name=self.label.font_name,  # type: ignore
            container_width=self.width,
            container_height=self.height,
        )
        self.label.font_size = optimal_font_size


class UIBlinkingLabel(gui.UILabel):
    """
    A Text Label that blinks (fades in and out) automatically.
    Configure using the `blink_*` and `fade_*` properties.
    To disable fading, set `do_fade` to `False`.
    """
    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        width: Optional[float] = None,
        height: Optional[float] = None,
        text: str = "",
        font_name: tuple[str, ...] = ('Arial',),
        font_size: float = 12,
        text_color: types.Color = types.Color(255, 255, 255, 255),
        bold: bool = False,
        italic: bool = False,
        align: str = 'left',
        multiline: bool = False,
        size_hint: Optional[tuple[float, float]] = None,
        size_hint_min: Optional[tuple[float, float]] = None,
        size_hint_max: Optional[tuple[float, float]] = None,
        **kwargs: Any
    ) -> None:
        """`arcade.gui.UILabel` constructor."""
        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height,
            text=text,
            font_name=font_name,
            font_size=font_size,
            text_color=text_color,
            bold=bold,
            italic=italic,
            align=align,
            multiline=multiline,
            size_hint=size_hint,
            size_hint_min=size_hint_min,
            size_hint_max=size_hint_max,
            **kwargs,
        )

        # Set property defaults
        self._blink_speed: float = 1.0
        self._fade_min: int = 0
        self._fade_max: int = 255
        self._do_fade: bool = True

        self._opacity: float = 255.0
        self._fade_direction: Literal["up", "down"] = "down"

    @property
    def blink_speed(self) -> float:
        """
        Time between `fade_min` and `fade_max` in seconds.
        0 means disabled, defaults to 1.
        """
        return self._blink_speed

    @blink_speed.setter
    def blink_speed(self, value: float) -> None:
        self._blink_speed = value

    @property
    def fade_min(self) -> int:
        """
        Minimum opacity the text may fade to. From 0 to 255.
        Defaults to 0.
        """
        return self._fade_min

    @fade_min.setter
    def fade_min(self, value: int) -> None:

        if value < 0:
            raise ValueError(
                "Value for `fade_min` should be no less than 0 "
                f"(got {value})."
            )
        elif value < self.fade_min:
            raise ValueError(
                f"`fade_min` ({value}) can't be higher than `fade_max` "
                f"({self.fade_max})."
            )

        self._opacity = value if self._opacity < value else self._opacity

        self._fade_min = value

    @property
    def fade_max(self) -> int:
        """
        Maximum opacity the text may fade to. From 0 to 255.
        Defaults to 255
        """
        return self._fade_max

    @fade_max.setter
    def fade_max(self, value: int) -> None:

        if value > 255:
            raise ValueError(
                "Value for `fade_max` should be no more than 255 "
                f"(got {value})."
            )
        elif value < self.fade_min:
            raise ValueError(
                f"`fade_max` ({value}) can't be lower than `fade_min` "
                f"({self.fade_min})."
            )

        self._opacity = value if self._opacity > value else self._opacity

        self._fade_max = value

    @property
    def do_fade(self) -> bool:
        """
        If the Label should fade at all or just jump from `fade_min` to
        `fade_max` directly.

        If True all `fade_*` properties are ignored.
        Defaults to False.
        """
        return self._do_fade

    @do_fade.setter
    def do_fade(self, value: bool) -> None:
        self._do_fade = value

    def on_update(self, delta_time: float) -> None:
        if self.blink_speed <= 0:
            return

        # Calculate s (distance)
        distance_min_max = self.fade_max - self.fade_min
        # Calculate v (velocity)
        opacity_per_second = distance_min_max / self.blink_speed
        # Calculate t (time) in this case the value to be added to self.opacity
        # while taking into account the delta_time
        opacity_increment = opacity_per_second * delta_time
        # NOTE: For some reason all tests failed because the above line was
        # opacity_increment = distance_min_max/opacity_per_second*delta_time
        # Removing the distance_min_max/ fixed them, I'm unsure why that was
        # there. If anyone knows please tell.

        if self._fade_direction == "up":
            self._opacity += opacity_increment
        else:  # self._fade_direction == "down"
            self._opacity -= opacity_increment

        if self._opacity <= self.fade_min:
            self._opacity = self.fade_min
            self._fade_direction = "up"
        elif self._opacity >= self.fade_max:
            self._opacity = self.fade_max
            self._fade_direction = "down"

        # If do_fade is True, update anyway
        # Otherwise only if fade_min/fade_max was reached
        if self.do_fade or self._opacity in (self.fade_min, self.fade_max):
            r, g, b, _ = self.label.color
            self.label.color = types.Color(r, g, b, round(self._opacity))
