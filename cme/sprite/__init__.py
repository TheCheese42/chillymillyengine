"""
Provides Premade Sprite classes as well as the Base `arcade.Sprite` and
`arcade.SpriteList` classes.
"""

from arcade import (PhysicsEnginePlatformer, PhysicsEngineSimple,
                    PymunkPhysicsEngine, Scene, Sprite, SpriteList)

from .sprite import AnimatedSprite, AnimatedWalkingSprite

__all__ = [
    "AnimatedSprite",
    "AnimatedWalkingSprite",
    "PhysicsEnginePlatformer",
    "PhysicsEngineSimple",
    "PymunkPhysicsEngine",
    "Scene",
    "Sprite",
    "SpriteList",
]
