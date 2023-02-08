from __future__ import annotations

from pathlib import Path
from typing import Any, Literal, Optional

import arcade
from enums import Facing
from texture import load_texture


class AnimatedSprite(arcade.Sprite):
    """
    Provides Support for category based animations.
    Designed for internal use.

    Textures are provided and saved as a list of tuples per category. The
    tuples contain a sprite for each required facing directory. If you just
    require left and right facing it might be best for you to flip the textures
    while loading. For that use the `load_texture_pair()` function from this
    module.
    """

    def __init__(
        self,
        filename: Optional[str] = None,
        scale: float = 1,
        image_x: float = 0,
        image_y: float = 0,
        image_width: float = 0,
        image_height: float = 0,
        center_x: float = 0,
        center_y: float = 0,
        repeat_count_x: int = 1,  # Unused
        repeat_count_y: int = 1,  # Unused
        flipped_horizontally: bool = False,
        flipped_vertically: bool = False,
        flipped_diagonally: bool = False,
        hit_box_algorithm: Optional[str] = "Simple",
        hit_box_detail: float = 4.5,
        texture: Optional[arcade.Texture] = None,
        angle: float = 0,
    ) -> None:
        """
        `arcade.Sprite` constructor.

        Add textures afterwards with `texture_*` methods.
        `texture` parameter will be used as default.
        """

        super().__init__(
            filename=filename,  # type: ignore
            scale=scale,
            image_x=image_x,
            image_y=image_y,
            image_width=image_width,
            image_height=image_height,
            center_x=center_x,
            center_y=center_y,
            repeat_count_x=repeat_count_x,
            repeat_count_y=repeat_count_y,
            flipped_horizontally=flipped_horizontally,
            flipped_vertically=flipped_vertically,
            flipped_diagonally=flipped_diagonally,
            hit_box_algorithm=hit_box_algorithm,
            hit_box_detail=hit_box_detail,
            texture=texture,  # type: ignore
            angle=angle,
        )

        self.all_textures: dict[
            str, list[tuple[arcade.Texture, ...]]
        ]

        self._state: Optional[str] = None

        self._facing: Facing | int = Facing.RIGHT

    @property
    def state(self) -> Optional[str]:
        return self._state

    @state.setter
    def state(self, value: str) -> None:
        if value not in self.all_textures:
            raise ValueError(f"No textures found for state `{value}`")
        self._state = value
        self.cur_texture_index = 0

    @property
    def facing(self) -> Facing | int:
        return self._facing

    @facing.setter
    def facing(self, value: Facing | int) -> None:
        self._facing = value

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        """
        Updates the current texture by taking the next texture of the current
        state.
        This will always update, only call if the time is right.
        """
        if not self.state:
            raise RuntimeError(
                "Tried to update animation of Sprite without state"
            )

        self.cur_texture_index += 1
        try:
            self.texture = self.all_textures[self.state][
                self.cur_texture_index
            ][self.facing]
        except IndexError:
            self.cur_texture_index = 0
            self.texture = self.all_textures[self.state][
                self.cur_texture_index
            ][self.facing]

    def add_texture(
        self,
        texture: arcade.Texture | tuple[arcade.Texture, ...],
        category: str,
    ) -> None:
        """
        Add a texture to the sprite. category is commonly a string like
        `idling`, `walking`, `jumping`, etc.
        If given a tuple of Textures
        """

        if isinstance(texture, tuple):
            try:
                self.all_textures[category].append(texture)
            except KeyError:
                self.all_textures[category] = [texture]
        else:
            try:
                self.all_textures[category].append((texture,))
            except KeyError:
                self.all_textures[category] = [(texture,)]

    def add_textures(
        self, textures: dict[str, list[tuple[arcade.Texture, ...]]]
    ) -> None:
        """wwadwwwddawd
        Add multiple Textures to the sprite. `textures` parameter should be a
        dict with a str as key indicating the category and a list of Textures
        as value.
        """
        for category, texture_list in textures.items():
            for texture_tuple in texture_list:
                self.add_texture(texture_tuple, category)

    def clear_textures(self) -> None:
        """
        Clear all textures added to this sprite, excluding the default one.
        """
        self.all_textures.clear()


class AnimatedWalkingSprite(AnimatedSprite):
    """
    Adds out of the box support for idling und walking textures.
    Idles by default.
    """

    def __init__(
        self,
        filename: Optional[str] = None,
        scale: float = 1,
        image_x: float = 0,
        image_y: float = 0,
        image_width: float = 0,
        image_height: float = 0,
        center_x: float = 0,
        center_y: float = 0,
        repeat_count_x: int = 1,  # Unused
        repeat_count_y: int = 1,  # Unused
        flipped_horizontally: bool = False,
        flipped_vertically: bool = False,
        flipped_diagonally: bool = False,
        hit_box_algorithm: Optional[str] = "Simple",
        hit_box_detail: float = 4.5,
        texture: Optional[arcade.Texture] = None,
        angle: float = 0,
    ) -> None:
        """
        `arcade.Sprite` constructor.

        Add textures afterwards with `texture_*` methods.
        `texture` parameter will be used as default.
        """

        super().__init__(
            filename=filename,
            scale=scale,
            image_x=image_x,
            image_y=image_y,
            image_width=image_width,
            image_height=image_height,
            center_x=center_x,
            center_y=center_y,
            repeat_count_x=repeat_count_x,
            repeat_count_y=repeat_count_y,
            flipped_horizontally=flipped_horizontally,
            flipped_vertically=flipped_vertically,
            flipped_diagonally=flipped_diagonally,
            hit_box_algorithm=hit_box_algorithm,
            hit_box_detail=hit_box_detail,
            texture=texture,
            angle=angle,
        )

        self.state: Literal["idling", "walking"] = "idling"

    def set_idling(self) -> None:
        self.state = "idling"

    def set_walking(self) -> None:
        self.state = "walking"

    def texture_add_idling(
        self,
        textures: list[tuple[arcade.Texture, ...]],
    ) -> None:
        for texture in textures:
            self.add_texture(texture, "idling")

    def texture_add_walking(
        self,
        textures: list[tuple[arcade.Texture, ...]],
    ) -> None:
        for texture in textures:
            self.add_texture(texture, "walking")


def load_texture_pair(
    file_name: str | Path,
    **kwargs: Any,
) -> tuple[arcade.Texture, arcade.Texture]:
    """
    All`**kwargs` are passed to the `load_texture()` function and
    therefore applied to both textures. Don't use any `flipped_*` kwargs
    as they are internally used to flip the second sprite.
    """

    return (
        load_texture(file_name, **kwargs),
        load_texture(file_name, flipped_horizontally=True, **kwargs),
    )
