"""
Provides pre-made Sprite classes as well as the Base `arcade.Sprite` (exported
as `ArcadeSprite`), `arcade.BasicSprite` and `arcade.SpriteList` classes. It
also provides an enhanced Sprite class which takes delta_time into account
when using `change_x`, `change_y` or `change_angle`.
"""

from arcade import (BasicSprite, PhysicsEnginePlatformer, PhysicsEngineSimple,
                    PymunkPhysicsEngine, Scene)
from arcade import Sprite as ArcadeSprite
from arcade import (SpriteList, check_for_collision,
                    check_for_collision_with_list,
                    check_for_collision_with_lists)

from .animator import Animator
from .sprite import (AnimatedSprite, AnimatedWalkingSprite, SimpleUpdater,
                     Sprite, StrictCollisionUpdater, TopDownUpdater, Updater,
                     WallBounceUpdater)

__all__ = [
    "AnimatedSprite",
    "AnimatedWalkingSprite",
    "Animator",
    "ArcadeSprite",
    "BasicSprite",
    "check_for_collision",
    "check_for_collision_with_list",
    "check_for_collision_with_lists",
    "PhysicsEnginePlatformer",
    "PhysicsEngineSimple",
    "PymunkPhysicsEngine",
    "Scene",
    "SimpleUpdater",
    "Sprite",
    "SpriteList",
    "StrictCollisionUpdater",
    "TopDownUpdater",
    "Updater",
    "WallBounceUpdater",
]
