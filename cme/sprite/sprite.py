from typing import Optional

import arcade


class AnimatedSprite(arcade.Sprite):
    """
    Provides Support for category based animations.
    Designed for internal use.
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

        self.all_textures: dict[str, list[arcade.Texture]]

    def texture_add(self, texture: arcade.Texture, category: str):
        """
        Add a texture to the sprite. category is commonly a string like
        `idle`, `walking`, `jumping`, etc.
        """
        try:
            self.all_textures[category].append(texture)
        except KeyError:
            self.all_textures[category] = [texture]

    def texture_add_multiple(self, textures: dict[str, list[arcade.Texture]]):
        """
        Add multiple Textures to the sprite. `textures` parameter should be a
        dict with a str as key indicating the category and a list of Textures
        as value.
        """
        for category, texture_list in textures.items():
            for texture in texture_list:
                self.texture_add(texture, category)

    def texture_clear(self):
        """
        Clear all textures added to this sprite, excluding the default one.
        """
        self.all_textures.clear()
