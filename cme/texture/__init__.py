"""
Exporting texture functions and classes from the arcade library.
"""

from arcade import Texture, load_texture, load_textures
from arcade.hitbox import (BoundingHitBoxAlgorithm, HitBox, HitBoxAlgorithm,
                           PymunkHitBoxAlgorithm, RotatableHitBox,
                           SimpleHitBoxAlgorithm, algo_bounding_box,
                           algo_default, algo_detailed, algo_simple,
                           calculate_hit_box_points_detailed,
                           calculate_hit_box_points_simple)

from .texture import load_texture_series

__all__ = [
    "BoundingHitBoxAlgorithm",
    "HitBox",
    "HitBoxAlgorithm",
    "PymunkHitBoxAlgorithm",
    "RotatableHitBox",
    "SimpleHitBoxAlgorithm",
    "algo_bounding_box",
    "algo_default",
    "algo_detailed",
    "algo_simple",
    "calculate_hit_box_points_detailed",
    "calculate_hit_box_points_simple",
    "load_texture",
    "load_texture_series",
    "load_textures",
    "Texture",
]
