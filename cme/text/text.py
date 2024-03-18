from typing import Optional, Union

from arcade import Text as ArcadeText
from arcade import csscolor
from arcade.types import RGBOrA
from pyglet.graphics import Batch, Group

from .. import logger
from ..utils import get_optimal_font_size


def center_x(text: ArcadeText, width: int) -> None:
    text.x = width / 2 - text.content_width / 2


def center_y(text: ArcadeText, height: int) -> None:
    text.y = height / 2 - text.content_height / 2


class Text(ArcadeText):
    """
    Enhanced Text class, supports using the biggest font for a given size
    """
    def set_optimal_font_size(
        self,
        text: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        max_size: Optional[float] = None,
    ):
        """Set the Text font size according to the provided sizes and text.
        If no values are passed, the ones stored in the Text object are used.

        Args:
            text (Optional[str], optional): Text to fit. Defaults to None.
            width (Optional[int], optional): Maximum width. Defaults to None.
            height (Optional[int], optional): Maximum height. Defaults to None.
            max_size (Optional[float], optional): Maximum size. Careful: If
            unset this will default to the current font size. If you need it as
            big as possible, 512 is recommendet. Defaults to None.
        """
        try:
            self.font_size = get_optimal_font_size(
                text=text or self.text,
                font_name=self.font_name,
                container_width=width or self.width,
                container_height=height or self.height,
                max_size=max_size or self.font_size,
                multiline=self.multiline,
            )
        except TypeError:
            logger.error(
                "Information required for optimal resizing of Text object not "
                "available (see trace)",
                exc_info=True,
            )


class PreconfiguredText(Text):
    """
    Class enabling Text objects with configurable default attributes. Set those
    by overwriting the DEFAULT_* attributes **on the class**!

    You also don't have to provide a text or position at first so you can set
    them later i.e. in an align method.
    """

    DEFAULT_FONT_SIZE: float = 0
    DEFAULT_FONT_NAME: Union[str, tuple[str, ...]] = "Arial"
    DEFAULT_COLOR: RGBOrA = csscolor.WHITE
    DEFAULT_ALIGN: str = "left"
    DEFAULT_BOLD: bool = False
    DEFAULT_ITALIC: bool = False
    DEFAULT_ANCHOR_X: str = "left"
    DEFAULT_ANCHOR_Y: str = "baseline"
    DEFAULT_MULTILINE: bool = False
    DEFAULT_ROTATION: float = 0

    def __init__(
        self,
        text: Optional[str] = None,
        start_x: int = 0,
        start_y: int = 0,
        color: Optional[RGBOrA] = None,
        font_size: Optional[float] = None,
        width: int = 0,
        align: Optional[str] = None,
        font_name: Optional[Union[str, tuple[str, ...]]] = None,
        bold: Optional[bool] = None,
        italic: Optional[bool] = None,
        anchor_x: Optional[str] = None,
        anchor_y: Optional[str] = None,
        multiline: Optional[bool] = None,
        rotation: Optional[float] = None,
        batch: Optional[Batch] = None,
        group: Optional[Group] = None,
        start_z: int = 0,
    ):
        if font_size is None:
            font_size = self.DEFAULT_FONT_SIZE
        if font_name is None:
            font_name = self.DEFAULT_FONT_NAME
        if color is None:
            color = self.DEFAULT_COLOR
        if align is None:
            align = self.DEFAULT_ALIGN
        if bold is None:
            bold = self.DEFAULT_BOLD
        if italic is None:
            italic = self.DEFAULT_ITALIC
        if anchor_x is None:
            anchor_x = self.DEFAULT_ANCHOR_X
        if anchor_y is None:
            anchor_y = self.DEFAULT_ANCHOR_Y
        if multiline is None:
            multiline = self.DEFAULT_MULTILINE
        if rotation is None:
            rotation = self.DEFAULT_ROTATION

        super().__init__(
            text,
            start_x,
            start_y,
            color,
            font_size,
            width,
            align,
            font_name,
            bold,
            italic,
            anchor_x,
            anchor_y,
            multiline,
            rotation,
            batch,
            group,
            start_z,
        )


class HeadlineText(PreconfiguredText):
    DEFAULT_FONT_SIZE = 60


class NormalText(PreconfiguredText):
    DEFAULT_FONT_SIZE = 18
