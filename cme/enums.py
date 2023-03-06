"""
Holds all enumerations.
"""

from enum import Enum


class Facing(Enum):
    """
    Holds enums for common facing directories.
    Subclass to add your own.
    """
    RIGHT = 0
    LEFT = 1
    FRONT = 2
    BACK = 3
