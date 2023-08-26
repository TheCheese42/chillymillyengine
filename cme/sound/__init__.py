"""
Provides sound utility functions.
"""

from .sound import (get_all_player_instances, is_music, is_sound, load_sound,
                    pause_all_sounds, play_sound, resume_all_sounds,
                    stop_all_sounds, stop_sound)

__all__ = [
    "get_all_player_instances",
    "is_music",
    "is_sound",
    "load_sound",
    "pause_all_sounds",
    "play_sound",
    "resume_all_sounds",
    "stop_all_sounds",
    "stop_sound",
]
