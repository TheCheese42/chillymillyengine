"""
Single threaded concurrency solutions to schedule functions.
"""


from typing import Any, Callable
from numbers import Number

import arcade


def schedule_once(func: Callable, time: float) -> None:
    """
    Schedule a function to execute once after `time` seconds. The scheduled
    function's first argument must be a float `delta_time` to represent the
    time elapsed since it has been scheduled.
    """
    # As for arcade 3.6.17 this requires the development branch to be installed
    arcade.schedule_once(func, time)


def schedule_interval(func: Callable, time: float) -> None:
    """
    Schedule to execute in intervals after `time` seconds. The scheduled
    function's first argument must be a float `delta_time` to represent the
    time elapsed since it has been scheduled. Don't forget to unschedule later.
    """
    arcade.schedule(func, time)


def unschedule(func: Callable) -> None:
    """
    Unschedule a given function object.
    """
    arcade.unschedule(func)
