"""
Contains several specific pre-made Sprite classes.
"""


from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Iterable, Optional

import arcade
from arcade.types import Rect

from .. import logger
from ..enums import Facing
from ..texture import load_texture
from ..utils import point_in_rect


class Updater:
    def update(self, sprite: arcade.Sprite, delta_time: float) -> None:
        raise NotImplementedError("update() should be overridden by subclass")


class SimpleUpdater(Updater):
    """Just move, taking delta_time into account."""

    def update(self, sprite: arcade.Sprite, delta_time: float) -> None:
        sprite.center_x += sprite.change_x * delta_time
        sprite.center_y += sprite.change_y * delta_time
        sprite.angle += sprite.change_angle * delta_time


class StrictCollisionUpdater(Updater):
    """
    Move taking delta_time into account, cancelling movement into a specific
    direction when a collision with a wall happens.
    This can be overridden to enhance mechanics, for example to add border
    handling
    """

    def __init__(self, walls: arcade.SpriteList[Sprite]):
        self.walls = walls

    def update(self, sprite: arcade.Sprite, delta_time: float) -> None:
        sprite.center_x += sprite.change_x * delta_time
        if arcade.check_for_collision_with_list(sprite, self.walls):
            sprite.center_x -= sprite.change_x * delta_time

        sprite.center_y += sprite.change_y * delta_time
        if arcade.check_for_collision_with_list(sprite, self.walls):
            sprite.center_y -= sprite.change_y * delta_time

        sprite.angle += sprite.change_angle * delta_time
        if arcade.check_for_collision_with_list(sprite, self.walls):
            sprite.angle -= sprite.change_angle * delta_time


class TopDownUpdater(Updater):
    """
    Move taking delta_time into account. For top movement, check center
    collision. For down and sideways movement, strictly check for collisions.
    For angles this uses strict collision checks as well.
    Also takes borders into account.
    """

    def __init__(self, walls: arcade.SpriteList[Sprite], border: Rect):
        self.walls = walls
        self.border = border

    def update(self, sprite: arcade.Sprite, delta_time: float) -> None:
        prev_x = sprite.center_x
        sprite.center_x += sprite.change_x * delta_time
        if (
            sprite.change_x > 0 and
            not point_in_rect(sprite.right, sprite.center_y, self.border)
            or sprite.change_x < 0 and
            not point_in_rect(sprite.left, sprite.center_y, self.border)
        ):
            sprite.center_x = prev_x
        for wall in arcade.check_for_collision_with_list(
            sprite, self.walls
        ) if sprite.center_x != prev_x else []:  # No check if standing still
            # Does NOT break the rules due to top wall handling
            if sprite.center_y > wall.bottom:
                if (
                    sprite.change_x > 0 and sprite.right > wall.left
                    or sprite.change_x < 0 and sprite.left < wall.right
                ):
                    sprite.center_x = prev_x
                    break

        prev_y = sprite.center_y
        sprite.center_y += sprite.change_y * delta_time
        if (
            sprite.change_y > 0 and
            not point_in_rect(sprite.center_x, sprite.top, self.border)
            or sprite.change_y < 0 and
            not point_in_rect(sprite.center_x, sprite.bottom, self.border)
        ):
            sprite.center_y = prev_y
        for wall in arcade.check_for_collision_with_list(
            sprite, self.walls
        ) if sprite.center_y != prev_y else []:  # No check if standing still
            # Does NOT break the rules due to top wall handling
            if sprite.center_y > wall.bottom:
                if (
                    sprite.change_y > 0 and sprite.center_y > wall.bottom
                    or sprite.change_y < 0 and sprite.bottom < wall.top
                ):
                    sprite.center_y = prev_y
                    break

        prev_angle = sprite.angle
        sprite.angle = sprite.change_angle * delta_time
        for wall in arcade.check_for_collision_with_list(sprite, self.walls):
            # Does NOT break the rules due to top wall handling
            if sprite.center_y > wall.bottom:
                sprite.angle = prev_angle
                break


class Sprite(arcade.Sprite):
    """
    Enhances change_x, change_y and change_angle by multiplying with
    timedelta. Should generally be taken over ArcadeSprite.
    """
    def update(self) -> None:
        """
        Overriding due to the fact that arcade's default behavior updates
        Sprite positions while not taking delta_time into account.
        This does nothing. Logic is now in `on_update()`.
        """
        pass

    def on_update(  # type: ignore[override]  # (Save because it only adds a default argument)  # noqa
        self,
        delta_time: float,
        updater: Updater = SimpleUpdater(),
    ) -> None:
        """
        This method moves the sprite based on its velocity and angle change.
        Takes delta_time into account by multiplying it with the change values.
        """
        updater.update(self, delta_time)

    @property
    def center(self) -> tuple[float, float]:
        return (self.center_x, self.center_y)

    @center.setter
    def center(self, point: tuple[float, float]) -> None:
        self.center_x = point[0]
        self.center_y = point[1]


class AnimatedSprite(Sprite):
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
        path_or_texture: Optional[str | arcade.Texture] = None,
        scale: float = 1,
        center_x: float = 0,
        center_y: float = 0,
        angle: float = 0,
    ) -> None:
        """
        `arcade.Sprite` constructor.

        Add textures afterwards with `texture_*` methods.
        `path_or_texture` parameter will be used as default.
        """
        super().__init__(
            path_or_texture=path_or_texture,
            scale=scale,
            center_x=center_x,
            center_y=center_y,
            angle=angle,
        )

        self.initial_texture_set = bool(path_or_texture)

        self.all_textures: dict[
            str, list[tuple[arcade.Texture, ...]]
        ] = {}

        self._state: Optional[str] = None

        self._facing: Facing | int = Facing.RIGHT

        self._animation_speed: float = 1
        self._last_animation_update = time.time()

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

    @property
    def animation_speed(self) -> float:
        """Time between animation updates in seconds."""
        return self._animation_speed

    @animation_speed.setter
    def animation_speed(self, value: int) -> None:
        self._animation_speed = value

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        """
        Updates the current texture by taking the next texture of the current
        state.
        This will update based on the specified `animation_speed` attribute.
        """

        if not self.state:
            raise RuntimeError(
                "Tried to update animation of Sprite without state"
            )

        current_time = time.time()
        if current_time - self._last_animation_update >= self.animation_speed:
            self.cur_texture_index += 1
            self._last_animation_update = current_time

            try:
                differently_faced_textures = self.all_textures[self.state][
                    self.cur_texture_index
                ]
            except IndexError:
                self.cur_texture_index = 0
                differently_faced_textures = self.all_textures[self.state][
                    self.cur_texture_index
                ]
            try:
                self.texture = differently_faced_textures[
                    self.facing
                ]
            except IndexError:
                self.texture = differently_faced_textures[0]
                logger.error(
                    "Tried to update animation on Sprite with unavailable "
                    "facing, falling back to index 0.",
                    exc_info=True
                )

        self.sync_hit_box_to_texture()  # type: ignore[no-untyped-call]

    def add_texture(
        self,
        texture: arcade.Texture | tuple[arcade.Texture, ...],
        category: str,
    ) -> None:
        """
        Add a texture to the sprite. category is commonly a string like
        `idling`, `walking`, `jumping`, etc.
        If given a tuple of Textures, multiple facing directories are stored
        and can later be accessed using the Facing enum from the enums module.
        """
        # Prevent weird Texture before first animation tick
        if not self.initial_texture_set:
            if isinstance(texture, tuple):
                self.texture = texture[0]
            else:
                self.texture = texture
            self.initial_texture_set = True

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
        """
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

    Textures are provided and saved as a list of tuples per category. The
    tuples contain a sprite for each required facing directory. If you just
    require left and right facing it might be best for you to flip the textures
    while loading. For that use the `load_texture_pair()` function from this
    module.
    """

    def __init__(
        self,
        path_or_texture: Optional[str] = None,
        scale: float = 1,
        center_x: float = 0,
        center_y: float = 0,
        angle: float = 0,
    ) -> None:
        """
        `arcade.Sprite` constructor.

        Add textures afterwards with `texture_*` methods.
        `texture` parameter will be used as default.
        """

        super().__init__(
            path_or_texture=path_or_texture,
            scale=scale,
            center_x=center_x,
            center_y=center_y,
            angle=angle,
        )

    def set_idling(self) -> None:
        self.state = "idling"

    def set_walking(self) -> None:
        self.state = "walking"

    def texture_add_idling(
        self,
        textures: list[tuple[arcade.Texture, ...]],
    ) -> None:
        """
        Adds a list containing tuples of Textures and assigns them as idling
        textures.

        Obtain the Structure by collecting left-right faced texture tuples from
        `load_texture_pair()` in a list.
        If you only need one Texture for all possible facings or aren't using
        different facing directions at all, simply pass one-item tuples to the
        function.
        """
        for texture in textures:
            self.add_texture(texture, "idling")

    def texture_add_walking(
        self,
        textures: list[tuple[arcade.Texture, ...]],
    ) -> None:
        """
        Adds a list containing tuples of Textures and assigns them as walking
        textures.

        Obtain the Structure by collecting left-right texture tuples from
        `load_texture_pair()` in a list.
        If you only need one Texture for all possible facings or aren't using
        different facing directions at all, simply pass one-item tuples to the
        function.
        """
        for texture in textures:
            self.add_texture(texture, "walking")


def load_texture_pair(
    file_name: str | Path,
    **kwargs: Any,
) -> tuple[arcade.Texture, arcade.Texture]:
    """
    All `**kwargs` are passed to the `load_texture()` function and
    therefore applied to both textures. Don't use any `flipped_*` kwargs
    as they are internally used to flip the second sprite.
    """

    return (
        texture := load_texture(file_name, **kwargs),
        texture.flip_horizontally(),
    )
