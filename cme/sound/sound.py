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
    streaming: bool = False,
    is_music: bool = False,
) -> Optional[arcade.Sound]:
    """
    `streaming` parameter should be True for very long music
    and False otherwise.
    """
    sound = arcade.load_sound(path=path, streaming=streaming)
    sound.is_music = is_music
    return sound


def play_sound(
    sound: arcade.Sound,
    volume: int,
    pan: float = 0,
    looping: bool = False,
    speed: float = 1,
) -> Player:
    """
    `volume` should be between 0 and 1.
    This wrapper function exists to force the programmer to provide a volume.
    """
    player = arcade.play_sound(
        sound=sound,
        volume=volume,
        pan=pan,
        looping=looping,
        speed=speed,
    )
    player.is_music = sound.is_music if hasattr(sound, "is_music") else False


def stop_sound(player: Player) -> None:
    """Exists to complete the sound control set."""
    arcade.stop_sound(player)


def is_music(player_or_sound: Player | arcade.Sound):
    if not hasattr(player_or_sound, "is_music"):
        return False
    return player_or_sound.is_music


def is_sound(player_or_sound: Player | arcade.Sound):
    if not hasattr(player_or_sound, "is_music"):
        return True
    return not player_or_sound.is_music


def pause_all_sounds() -> None:
    """Pauses all playing players."""
    for player in get_all_player_instances():
        player.pause()


def resume_all_sounds() -> None:
    """Resumes all paused players."""
    for player in get_all_player_instances():
        player.play()


def stop_all_sounds() -> None:
    """Stops all playing players."""
    for player in get_all_player_instances():
        stop_sound(player)


def get_all_player_instances() -> list[Player]:
    """Retrieve a list of player instances."""
    return [obj for obj in gc.get_objects() if isinstance(obj, Player)]
