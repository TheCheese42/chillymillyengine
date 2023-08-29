"""
Provides an interface to manage game saves. For flexibility and to allow
multiple types of saves to exist, no special load and save functionality is
provided.
"""


from __future__ import annotations

import abc
import json
from pathlib import Path
from typing import Any, Optional

from .paths import DATA_PATH


class GameSave(metaclass=abc.ABCMeta):
    """
    Interface class for managing game saves and serializing them into json
    files.

    Subclass this and implement the unimplemented methods:

    `update()`, `_serialize()`

    Unimplemented classmethods:

    `_deserialize()`

    Unimplemented staticmethods:

    `defaults()`
    """

    @classmethod
    def __subclasshook__(cls, subclass: Any) -> Any:
        return (
            hasattr(subclass, "from_file")
            and callable(subclass.from_file)
            and hasattr(subclass, "from_json")
            and callable(subclass.from_json)
            and hasattr(subclass, "defaults")
            and callable(subclass.defaults)
            and hasattr(subclass, "_deserialize")
            and callable(subclass._deserialize)
            and hasattr(subclass, "_serialize")
            and callable(subclass._serialize)
            and hasattr(subclass, "update")
            and callable(subclass.update)
            and hasattr(subclass, "with_defaults")
            and callable(subclass.with_defaults)
            and hasattr(subclass, "save_to_file")
            and callable(subclass.save_to_file)
            or NotImplemented
        )

    @classmethod
    def from_file(cls, file: str | Path) -> GameSave:
        """Instantiates the class from a json file."""
        with open(file, mode="r") as fp:
            return cls.from_json(fp.read())

    @classmethod
    def from_json(cls, json_str: str) -> GameSave:
        """Instantiates the class from a json string."""
        return cls._deserialize(json.loads(json_str))

    @staticmethod
    @abc.abstractmethod
    def defaults() -> dict[str, Any]:
        """
        Returns a dictionary containing a serialized GameSave object
        with default values.
        """
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def _deserialize(cls, dictionary: dict[str, Any]) -> GameSave:
        """Instantiates the class from a serialized dictionary."""
        raise NotImplementedError

    @abc.abstractmethod
    def _serialize(self) -> dict[str, Any]:
        """Serializes the object into a dictionary."""
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, **kwargs: Any) -> None:
        """Updates multiple entries at once."""
        raise NotImplementedError

    @classmethod
    def with_defaults(cls) -> GameSave:
        """Returns an instance of the class with default settings."""
        return cls._deserialize(cls.defaults())

    def save_to_file(self, file: str | Path) -> None:
        with open(file, "w") as fp:
            json.dump(self._serialize(), fp)


def load_game_save(
    game_save_class: type[GameSave],
    profile: Optional[str] = None,
) -> GameSave:
    """
    Load GameSave object from standard directory.
    Optionally takes a profile name to support multiple accounts/profiles.
    """
    filename = "gamesave.json" if not profile else f"gamesave_{profile}.json"
    return game_save_class.from_file(DATA_PATH / "saves" / filename)


def save_game_save(game_save: GameSave, profile: Optional[str] = None) -> None:
    """
    Save the given GameSave object to the standard directory.
    Optionally takes a profile name to suppport multiple accounts/profiles.
    """
    filename = "gamesave.json" if not profile else f"gamesave_{profile}.json"
    game_save.save_to_file(DATA_PATH / "saves" / filename)
