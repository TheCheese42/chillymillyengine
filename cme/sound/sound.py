"""
Wrapping the sound functions from the arcade library to force
the programmer to provide a volume value. If this behavior is
unwanted just directly access the functions provided by arcade.

Also includes convenience functions to pause or stop all playing sounds.
This works by using the gc module, don't use if it causes lag spikes.
"""

from __future__ import annotations

import gc
from pathlib import Path
from typing import Optional

import arcade
from pyglet.media import Player


def load_sound(
    path: str | Path,
    streaming: bool = False
) -> Optional[arcade.Sound]:
    """
    `streaming` parameter should be True for very long music
    and False otherwise.
    """
    return arcade.load_sound(path=path, streaming=streaming)


def play_sound(
    sound: arcade.Sound,
    volume: int,
    pan: float = 0,
    looping: bool = False,
    speed: float = 1
) -> Player:
    """
    `volume` should be between 0 and 1.
    This wrapper function exists to force the programmer to provide a volume.
    """
    return arcade.play_sound(
        sound=sound,
        volume=volume,
        pan=pan,
        looping=looping,
        speed=speed,
    )


def stop_sound(player: Player) -> None:
    """Exists to complete the sound control set."""
    return arcade.stop_sound(player)


def pause_all_sounds() -> None:
    """Pauses all playing players"""
    for obj in gc.get_objects():
        if isinstance(obj, Player):
            obj.pause()


def resume_all_sounds() -> None:
    """Resumes all paused players"""
    for obj in gc.get_objects():
        if isinstance(obj, Player):
            obj.play()


def stop_all_sounds() -> None:
    """Stops all playing players"""
    for obj in gc.get_objects():
        if isinstance(obj, Player):
            stop_sound(obj)
