"""
Provides Premade Sprite classes as well as the Base `arcade.Sprite` and
`arcade.SpriteList` classes.
"""

from arcade import Sprite, SpriteList

from .sprite import AnimatedSprite, AnimatedWalkingSprite

__all__ = [
    "AnimatedSprite",
    "AnimatedWalkingSprite",
    "Sprite",
    "SpriteList",
]
