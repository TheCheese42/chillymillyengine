"""
Defines custom gui elements.
"""
from __future__ import annotations

from typing import Any, Iterable, Literal, Mapping, Optional

from arcade import gui, types
from arcade.gui.nine_patch import NinePatchTexture
from arcade.gui.style import UIStyleBase
from arcade.gui.surface import Surface
from arcade.math import get_distance

from cme import csscolor, key, shapes
from cme.texture import Texture
from cme.utils import get_optimal_font_size, point_in_rect


class UIFixedSizeLabel(gui.UILabel):
    def __init__(
        self,
        max_font_size: int = 512,
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
        self.max_font_size = max_font_size

    def fit_content(self) -> None:
        raise AttributeError(f"Cannot resize {self.__class__.__name__}.")

    def update_text_size(self) -> None:
        """Sets the Text to the maximum possible size for the widget size."""
        font_name = self.label.font_name
        if isinstance(font_name, tuple):
            font_name = font_name[0]
        optimal_font_size = get_optimal_font_size(
            text=self.text,
            font_name=font_name,
            container_width=self.width,
            container_height=self.height,
            max_size=self.max_font_size
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


class UIToolTipButton(gui.UITextureButton):
    def __init__(
        self,
        tooltip_text: str,
        tooltip_font_name: str | tuple[str, ...] = ("calibri", "arial"),
        tooltip_font_size: int = 12,
        tooltip_color: tuple[int, int, int, int] = csscolor.BLACK,
        x: float = 0,
        y: float = 0,
        width: Optional[float] = None,
        height: Optional[float] = None,
        texture: Texture | NinePatchTexture | None = None,
        texture_hovered: Texture | NinePatchTexture | None = None,
        texture_pressed: Texture | NinePatchTexture | None = None,
        texture_disabled: Texture | NinePatchTexture | None = None,
        text: str = "",
        multiline: bool = False,
        scale: Optional[float] = None,
        style: Optional[dict[str, UIStyleBase]] = None,
        **kwargs: Mapping[Any, Any],
    ):
        """Create a button displaying a tooltip on hover.

        Args:
            tooltip_text (str): Text if the tooltip.
            tooltip_font_name (str | tuple, optional): The font used for the
            tooltip. Defaults to None.
            tooltip_font_size (int, optional): The font size used for the
            tooltip. Defaults to 12.
            tooltip_color (tuple[int, int, int, int], optional): The text color
            used for the tooltip. Defaults to csscolor.BLACK.
            tooltip_width (int, optional): Width of the tooltip. If 0 it sizes
            automatically. Defaults to 0.
            tooltip_multiline (bool, optional): Wether or not the tooltip
            should span multiple lines. If True, tooltip_width must be < 0.
            Rest is UITextureButton constructor.

        After construction one should add the tooltip label to the ui manager
        using .get_label(). Should also set its position using the .center
        property.
        """
        super().__init__(
            x,
            y,
            width,
            height,
            texture,
            texture_hovered,
            texture_pressed,
            texture_disabled,
            text,
            multiline,
            scale,
            style,
            **kwargs,
        )
        self._tooltip_label = gui.UILabel(
            width=200,
            text=tooltip_text,
            font_name=tooltip_font_name,
            font_size=tooltip_font_size,
            text_color=tooltip_color,
            multiline=True,
        )
        self._tooltip_label.visible = False

    def get_label(self) -> gui.UILabel:
        """Returns an UILabel that should be assigned to the frame, menu or
        whatever top level widget.

        Returns:
            gui.UILabel: The label containing the tooltip.
        """
        return self._tooltip_label

    def do_render(self, surface: Surface) -> None:
        super().do_render(surface)
        if self.get_current_state() == "hover":
            self._tooltip_label.visible = True
        else:
            self._tooltip_label.visible = False


class UITextureMessageBox(gui.UIMouseFilterMixin, gui.UIAnchorLayout):
    """
    A simple message box dialog with custom texture and buttons.
    Subscribe to `on_action` to get notified when the box is closed.
    """
    def __init__(
        self,
        text: str,
        menu_texture: Texture,
        button_texture: Texture,
        button_texture_hover: Optional[Texture] = None,
        button_texture_pressed: Optional[Texture] = None,
        font_name: str | tuple[str, ...] = ("calibri", "arial"),
        font_size: int = 12,
        text_color: tuple[int, int, int, int] = csscolor.BLACK,
        button_font_name: Optional[str | tuple[str, ...]] = None,
        button_font_size: Optional[int] = None,
        button_text_color: Optional[tuple[int, int, int, int]] = None,
        width: int = 0,
        height: int = 0,
        button_width: int = 0,
        button_height: int = 0,
        buttons: Iterable[str] = ("Ok",),
        box_border_width: int = 20,
        button_border_width: int = 5,
        scale: float = 1,
    ):
        """
        Args:
            text (str): The text to be displayed as message.
            font_name (str | tuple, optional): The font name for the text.
            Defaults to ("calibri", "arial").
            font_size (int, optional): The font size for the text. Defaults to
            12.
            text_color (tuple[int, int, int, int], optional): The text color.
            Defaults to csscolor.BLACK.
            button_font_name (str | tuple, optional): The font name for the
            button text. Defaults to the regular font name.
            button_font_size (int, optional): The font size for the button
            text. Defaults to the regular font size.
            button_text_color (tuple[int, int, int, int], optional): The text
            color. Defaults to the regular text color.
            width (int, optional): The width of the box. If unset it will take
            the texture size. Defaults to 0.
            height (int, optional): The height of the box. If unset it will
            take the texture size. Defaults to 0.
            buttons (Iterable, optional): An Iterable of buttons. Defaults to
            ("Ok",).

        Raises:
            ValueError: Requires at least one button to be set.
        """
        if not buttons:
            raise ValueError(
                "At least a single value has to be available for `buttons`"
            )

        super().__init__(size_hint=(1, 1))
        self.register_event_type("on_action")

        if not button_texture_hover:
            button_texture_hover = button_texture
        if not button_texture_pressed:
            button_texture_pressed = button_texture
        if not width:
            width = menu_texture.width
        if not height:
            height = menu_texture.height
        if not button_font_name:
            button_font_name = font_name
        if not button_font_size:
            button_font_size = font_size
        if not button_text_color:
            button_text_color = text_color
        if not button_width:
            button_width = button_texture.width
        if not button_height:
            button_height = button_texture.height

        for texture in (
            button_texture,
            button_texture_hover,
            button_texture_pressed
        ):
            texture.width = button_width
            texture.height = button_height

        # setup frame which will act like the window
        frame = self.add(
            gui.UIAnchorLayout(
                width=width * scale, height=height * scale, size_hint=None
            )
        )
        frame.with_padding(
            top=box_border_width + 10,
            right=box_border_width + 10,
            bottom=box_border_width + 10,
            left=box_border_width + 10,
        )

        frame.with_background(texture=NinePatchTexture(
            left=box_border_width,
            right=box_border_width,
            bottom=box_border_width,
            top=box_border_width,
            texture=menu_texture,
        ))

        # Setup text
        frame.add(
            child=gui.UITextArea(
                text=text,
                width=width * scale - box_border_width,
                height=height * scale - box_border_width,
                font_name=font_name,
                font_size=font_size,
                text_color=text_color,
            ),
            anchor_x="center",
            anchor_y="top",
        )

        # setup buttons
        button_group = gui.UIBoxLayout(vertical=False, space_between=10)
        button_style = gui.UITextureButtonStyle(
            font_size=button_font_size,
            font_name=button_font_name,
            font_color=button_text_color,
            border_width=button_border_width,
        )
        for button_text in buttons:
            button = gui.UITextureButton(
                texture=button_texture,
                texture_hovered=button_texture_hover,
                texture_pressed=button_texture_pressed,
                text=button_text,
                scale=scale,
                style={
                    "normal": button_style,
                    "hover": button_style,
                    "press": button_style,
                    "disabled": button_style,
                }
            )
            button_group.add(button)
            button.on_click = self._on_choice  # type: ignore

        frame.add(
            child=button_group,
            anchor_x="right",
            anchor_y="bottom",
        )

    def _on_choice(self, event: gui.UIOnClickEvent) -> None:
        if self.parent:
            self.parent.remove(self)
        self.dispatch_event(
            "on_action", gui.UIOnActionEvent(self, event.source.text)
        )

    def on_action(self, event: gui.UIOnActionEvent) -> None:
        """
        Called when button was pressed. Access the button text using
        `event.action`.
        """
        pass


class UIHoverOverlay(gui.UIMouseFilterMixin, gui.UIAnchorLayout):
    """
    A simple message box dialog with custom texture and buttons.
    Subscribe to `on_action` to get notified when the box is closed.
    """
    def __init__(
        self,
        text: str,
        texture: Texture,
        rect: types.Rect,
        width: int = 0,
        height: int = 0,
        font_name: str | tuple[str, str] = ("calibri", "arial"),
        font_size: int = 12,
        text_color: tuple[int, int, int, int] = csscolor.BLACK,
        texture_border_width: int = 10,
        texture_border_height: int = 10,
        scale: float = 1.0,
        offset_x: int = -5,
        offset_y: int = -5,
    ):
        """An overlay only showing when hovering over certain things, following
        the mouse.

        Args:
            text (str): The text to show.
            texture (Texture): The texture to use as background.
            rect (Rect): The Rectangle where mouse hover triggers the overlay.
            width (int, optional): The overlay width. If 0, the optimal width
            is used. Defaults to 0.
            height (int, optional): The overlay height. If 0, the optimal
            height is used. Defaults to 0.
            font_name (str | tuple[str, str], optional): The font to use.
            Defaults to ("calibri", "arial").
            font_size (int, optional): The font size to use. Defaults to 12.
            text_color (tuple[int, int, int, int], optional): The text color to
            use. Defaults to csscolor.BLACK.
            texture_border_width (int, optional): The border width of the
            background texture. Defaults to 10.
            texture_border_height (int, optional): The border height of the
            background texture. Defaults to 10.
            scale (float, optional): Scaling for size and font size. Defaults
            to 1.0.
            offset_x (int, optional): The horizontal offset of the label
            compared to the mouse. Defaults to -5.
            offset_x (int, optional): The vertical offset of the label compared
            to the mouse. Defaults to -5.
        """
        super().__init__()
        self.offset_x = offset_x
        self.offset_y = offset_y
        self._trigger_rect = rect

        # setup frame which will act like the window
        frame = self.add(
            gui.UIAnchorLayout(
                width=width * scale, height=height * scale, size_hint=None
            )
        )
        frame.with_padding(
            top=texture_border_height + 10,
            right=texture_border_width + 10,
            bottom=texture_border_height + 10,
            left=texture_border_width + 10,
        )

        frame.with_background(texture=NinePatchTexture(
            top=texture_border_height,
            right=texture_border_width,
            bottom=texture_border_height,
            left=texture_border_width,
            texture=texture,
        ))

        # Setup text
        frame.add(
            child=gui.UILabel(
                width=width or None,
                height=height or None,
                text=text,
                font_name=font_name,
                font_size=font_size,
                text_color=text_color,
                multiline=True,
            ),
            anchor_x="center",
            anchor_y="center",
        )

    def on_event(self, event: gui.UIEvent) -> Optional[bool]:
        if isinstance(event, gui.UIMouseMovementEvent):
            if point_in_rect(int(event.x), int(event.y), self._trigger_rect):
                self.visible = True
                self.center = (
                    event.x + self.width / 2 + self.offset_x,
                    event.y + self.height / 2 + self.offset_y
                )
                return True
            else:
                self.visible = False
        return super().on_event(event)


class UIFineColoredSlider(gui.UIWidget):
    """
    Horizontal slider where every square can have it's own color.
    It's borderless so the height will be the height of the middle cursor,
    while the content will take half of this size.
    """
    value = gui.Property(0)
    hovered = gui.Property(False)
    pressed = gui.Property(False)
    disabled = gui.Property(False)

    def __init__(
        self,
        *,
        value: float = 0,
        min_value: float = 0,
        max_value: float = 255,
        x: float = 0,
        y: float = 0,
        width: float = 300,
        height: float = 20,
        colors: Optional[list[types.RGBA255]] = None,
        cursor_color: types.RGBA255 = csscolor.BLACK,
        cursor_outline_color: types.RGBA255 = csscolor.BLACK,
    ):
        if height // 2 % width:
            raise ValueError("height//2 should be a multiple of width")

        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height,
        )

        self.value = value
        self.vmin = min_value
        self.vmax = max_value

        self.cursor_radius = self.height
        self.slider_height = self.height // 2
        self.color_square_size = self.slider_height
        self.color_square_amount = self.width / self.color_square_size
        if colors is None:
            colors = [(0, 0, 0, 0) for _ in range(self.color_square_amount)]
        elif len(colors) != self.color_square_amount:
            raise ValueError(
                f"colors should be of length {self.color_square_amount}, got "
                f"{len(colors)}"
            )
        self.colors = colors

        self.cursor_color = cursor_color
        self.cursor_outline_color = cursor_outline_color

        # trigger render on value changes
        gui.bind(self, "value", self.trigger_full_render)
        gui.bind(self, "hovered", self.trigger_render)
        gui.bind(self, "pressed", self.trigger_render)
        gui.bind(self, "disabled", self.trigger_render)

        self.register_event_type("on_change")

    def get_current_state(self) -> str:
        """
        Returns the current state of the slider i.e disabled, press, hover
        or normal.
        """
        if self.disabled:
            return "disabled"
        elif self.pressed:
            return "press"
        elif self.hovered:
            return "hover"
        else:
            return "normal"

    def _x_for_value(self, value: float) -> float:
        x = self.rect.x
        nval = (value - self.vmin) / self.vmax
        return (  # type: ignore
            x
            + self.cursor_radius
            + nval * (self.width - 2 * self.cursor_radius)
        )

    @property
    def norm_value(self) -> float:
        """Normalized value between 0.0 and 1.0"""
        return (self.value - self.vmin) / self.vmax

    @norm_value.setter
    def norm_value(self, value: float) -> None:
        self.value = min(
            value * (self.vmax - self.vmin) + self.vmin, self.vmax
        )

    @property
    def value_x(self) -> float:
        """Returns the current value of the cursor of the slider."""
        return self._x_for_value(self.value)

    @value_x.setter
    def value_x(self, nx: float) -> None:
        cr = self.rect

        x = min(
            cr.right - self.cursor_radius, max(nx, cr.x + self.cursor_radius)
        )
        if self.width == 0:
            self.norm_value = 0
        else:
            self.norm_value = (x - cr.x - self.cursor_radius) / float(
                self.width - 2 * self.cursor_radius
            )

    def do_render(self, surface: Surface) -> None:
        self.prepare_render(surface)  # type: ignore

        slider_height = self.slider_height
        cursor_radius = self.cursor_radius

        slider_left_x = self._x_for_value(self.vmin)
        slider_right_x = self._x_for_value(self.vmax)
        cursor_center_x = self.value_x

        slider_center_y = self.height // 2
        slider_buttom_y = slider_center_y + (slider_height // 2)

        x = slider_left_x
        for color in self.colors:
            shapes.draw_xywh_rectangle_filled(
                slider_left_x,
                slider_buttom_y,
                width=self.color_square_size,
                height=self.color_square_size,
                color=color,
            )

        # cursor
        cursor_color = self.cursor_color
        cursor_outline_color = self.cursor_outline_color

        rel_cursor_x = cursor_center_x - self.rect.x
        shapes.draw_circle_filled(
            rel_cursor_x, slider_center_y, cursor_radius, cursor_color
        )
        shapes.draw_circle_filled(
            rel_cursor_x,
            slider_center_y,
            cursor_radius // 4,
            cursor_outline_color,
        )

    def _cursor_pos(self) -> tuple[float, float]:
        return self.value_x, int(self.y + self.height // 2)

    def _is_on_cursor(self, x: float, y: float) -> bool:
        cursor_center_x, cursor_center_y = self._cursor_pos()
        cursor_radius = self.cursor_radius
        distance_to_cursor = get_distance(
            x, y, cursor_center_x, cursor_center_y
        )
        return distance_to_cursor <= cursor_radius  # type: ignore

    def on_event(self, event: gui.UIEvent) -> Optional[bool]:
        if isinstance(event, gui.UIMouseMovementEvent):
            self.hovered = self._is_on_cursor(event.x, event.y)

        if isinstance(event, gui.UIMouseDragEvent):
            if self.pressed:
                old_value = self.value
                self.value_x = event.x
                self.dispatch_event(
                    "on_change", gui.UIOnChangeEvent(
                        self, old_value, self.value
                    )
                )

        if isinstance(event, gui.UIMousePressEvent):
            if self._is_on_cursor(event.x, event.y):
                self.pressed = True

        if isinstance(event, gui.UIMouseReleaseEvent):
            self.pressed = False

        return False

    def on_change(self, event: gui.UIOnChangeEvent) -> None:
        """
        To be implemented by the user, triggered when the cursor's value is
        changed.
        """
        pass


class UIKeybindPicker(gui.UIMouseFilterMixin, gui.UIAnchorLayout):
    """
    Popup dialog asking the user to select a keybind.
    """
    def __init__(
        self,
        text: str,
        default_keybind: int,
        menu_texture: Texture,
        button_texture: Texture,
        button_texture_hover: Optional[Texture] = None,
        button_texture_pressed: Optional[Texture] = None,
        font_name: str | tuple[str, ...] = ("calibri", "arial"),
        font_size: int = 12,
        text_color: tuple[int, int, int, int] = csscolor.BLACK,
        button_font_name: Optional[str | tuple[str, ...]] = None,
        button_font_size: Optional[int] = None,
        button_text_color: Optional[tuple[int, int, int, int]] = None,
        width: int = 300,
        height: int = 200,
        button_width: int = 0,
        button_height: int = 0,
        buttons: tuple[str, str] = ("Cancel", "Confirm"),
        box_border_width: int = 10,
        button_border_width: int = 5,
        scale: float = 1,
    ):
        """
        Args:
            text (str): A message to show the user.
            default_keybind (int): The pre-selected keybind-
            menu_texture (Texture): The menu texture to use for the whole
            popup.
            button_texture (Texture): The button Texture for apply and cancel.
            button_texture_hover (Optional[Texture], optional): The button
            texture for hover. Defaults to None.
            button_texture_pressed (Optional[Texture], optional): The button
            texture for press. Defaults to None.
            font_name (str | tuple[str, ...], optional): The font name to use
            for the message. Defaults to ("calibri", "arial").
            font_size (int, optional): The font size to use for the message.
            Defaults to 12.
            text_color (tuple[int, int, int, int], optional): The text color to
            use for the message. Defaults to csscolor.BLACK.
            button_font_name (Optional[str  |  tuple[str, ...]], optional): The
            font name to use for the button text. Defaults to None.
            button_font_size (Optional[int], optional): The font size to use
            for the button text. Defaults to None.
            button_text_color (Optional[tuple[int, int, int, int]], optional):
            The text color to use for the button text. Defaults to None.
            width (int, optional): The width of the whole popup. Defaults to
            300.
            height (int, optional): The height of the whole popup. Defaults to
            200.
            button_width (int, optional): The width of one button. Defaults to
            the texture width.
            button_height (int, optional): The height of one button. Defaults
            to the texture width.
            buttons (tuple[str, str], optional): A tuple of button texts.
            Usable for localization, first  one is cancel and second confirm.
            Defaults to ("Cancel", "Confirm").
            box_border_width (int, optional): The width of the popup's border.
            Defaults to 10.
            button_border_width (int, optional): The width of the button's
            border. Defaults to 5.
            scale (float, optional): Scale for everything. Defaults to 1.

        Raises:
            ValueError: Buttons parameter has a length different from 2.
        """
        if len(buttons) != 2:
            raise ValueError(
                "`buttons` should be of length 2"
            )

        super().__init__()
        self.selected_keybind = default_keybind
        self.register_event_type("on_action")

        if not button_texture_hover:
            button_texture_hover = button_texture
        if not button_texture_pressed:
            button_texture_pressed = button_texture
        if not width:
            width = menu_texture.width
        if not height:
            height = menu_texture.height
        if not button_font_name:
            button_font_name = font_name
        if not button_font_size:
            button_font_size = font_size
        if not button_text_color:
            button_text_color = text_color
        if not button_width:
            button_width = button_texture.width
        if not button_height:
            button_height = button_texture.height

        for texture in (
            button_texture,
            button_texture_hover,
            button_texture_pressed
        ):
            texture.width = button_width
            texture.height = button_height

        # setup frame which will act like the window
        frame = self.add(
            gui.UIAnchorLayout(
                width=width * scale, height=height * scale, size_hint=None
            )
        )
        frame.with_padding(
            top=box_border_width + 10,
            right=box_border_width + 10,
            bottom=box_border_width + 10,
            left=box_border_width + 10,
        )

        frame.with_background(texture=NinePatchTexture(
            left=box_border_width,
            right=box_border_width,
            bottom=box_border_width,
            top=box_border_width,
            texture=menu_texture,
        ))

        # Setup text
        frame.add(
            child=gui.UITextArea(
                text=text,
                width=width * scale - box_border_width,
                height=height * scale - box_border_width,
                font_name=font_name,
                font_size=font_size,
                text_color=text_color,
            ),
            anchor_x="center",
            anchor_y="top",
        )

        # Setup keybind area
        self.keybind_label = gui.UILabel(
            text=key.reverse_lookup[self.selected_keybind],
            font_name=font_name,
            font_size=font_size * 1.5,
            text_color=text_color,
        )
        frame.add(self.keybind_label, anchor_x="center", anchor_y="center")

        # setup buttons
        button_group = gui.UIBoxLayout(vertical=False, space_between=10)
        button_style = gui.UITextureButtonStyle(
            font_size=button_font_size,
            font_name=button_font_name,
            font_color=button_text_color,
            border_width=button_border_width,
        )
        for button_text in buttons:
            button = gui.UITextureButton(
                texture=button_texture,
                texture_hovered=button_texture_hover,
                texture_pressed=button_texture_pressed,
                text=button_text,
                scale=scale,
                style={
                    "normal": button_style,
                    "hover": button_style,
                    "press": button_style,
                    "disabled": button_style,
                }
            )
            button_group.add(button)
            button.on_click = self._on_choice  # type: ignore
            # Returns 1 if idx 1 else 0
            button.is_confirm = bool(buttons.index(button))

        frame.add(
            child=button_group,
            anchor_x="center",
            anchor_y="bottom",
        )

    def _on_choice(self, event: gui.UIOnClickEvent) -> None:
        if self.parent:
            self.parent.remove(self)
        self.dispatch_event(
            "on_action", gui.UIOnActionEvent(
                self,
                self.selected_keybind if event.source.is_confirm else "cancel"
            )
        )

    def on_event(self, event: gui.UIEvent) -> Optional[bool]:
        if isinstance(event, gui.UIKeyPressEvent):
            key_ = event.symbol
            self.selected_keybind = key_
            self.keybind_label.text = key.reverse_lookup[key_]
            return True
        return super().on_event(event)

    def on_action(self, event: gui.UIOnActionEvent) -> None:
        """
        Called when button was pressed. Access the button text using
        `event.action`.
        """
