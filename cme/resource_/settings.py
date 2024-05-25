"""
Provides an interface for a class to manage all settings of the game,
optionally with multiple accounts/profiles as well as convenience functions.

Register your implementation using the `register_custom_settings_class()`
decorator.
"""


from __future__ import annotations

import abc
import json
from pathlib import Path
from typing import Any, Optional

from cme import logger

from .paths import SETTINGS_PATH

# Saves a custom Settings class provided by the user
CUSTOM_SETTINGS_CLASS: Optional[type[Settings]] = None


class Settings(metaclass=abc.ABCMeta):
    """
    Interface class for managing settings and serializing them into json files.

    Subclass this and implement the unimplemented methods:

    `apply()`, `update()`, `_serialize()`

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
            and hasattr(subclass, "apply")
            and callable(subclass.apply)
            and hasattr(subclass, "with_defaults")
            and callable(subclass.with_defaults)
            and hasattr(subclass, "save_to_file")
            and callable(subclass.save_to_file)
            or NotImplemented
        )

    @classmethod
    def from_file(cls, file: str | Path) -> Settings:
        """Instantiates the class from a json file."""
        with open(file, mode="r") as fp:
            return cls.from_json(fp.read())

    @classmethod
    def from_json(cls, json_str: str) -> Settings:
        """Instantiates the class from a json string."""
        return cls._deserialize(json.loads(json_str))

    @staticmethod
    @abc.abstractmethod
    def defaults() -> dict[str, Any]:
        """
        Returns a dictionary containing a serialized Settings object
        with default values.
        """
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def _deserialize(cls, dictionary: dict[str, Any]) -> Settings:
        """Instantiates the class from a serialized dictionary."""
        raise NotImplementedError

    @abc.abstractmethod
    def _serialize(self) -> dict[str, Any]:
        """Serializes the object into a dictionary."""
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, *args: Any, **kwargs: Any) -> None:
        """Updates multiple settings at once."""
        raise NotImplementedError

    @abc.abstractmethod
    def apply(self, *args: Any, **kwargs: Any) -> None:
        """Applies the settings to the game."""
        raise NotImplementedError

    @classmethod
    def with_defaults(cls) -> Settings:
        """Returns an instance of the class with default settings."""
        return cls._deserialize(cls.defaults())

    def save_to_file(self, file: str | Path) -> None:
        with open(file, "w") as fp:
            json.dump(self._serialize(), fp)


def register_custom_settings_class(cls: type[Settings]) -> type[Settings]:
    """Decorate your custom Settings class with this."""
    global CUSTOM_SETTINGS_CLASS
    if CUSTOM_SETTINGS_CLASS is not None:
        logger.warning(
            f"Registering class {cls.__name__} as custom settings class "
            f"although {CUSTOM_SETTINGS_CLASS.__name__} already has been."
        )
    CUSTOM_SETTINGS_CLASS = cls
    return cls


def load_settings(profile: Optional[str] = None) -> Settings:
    """
    Load Settings object from standard directory.
    Optionally takes a profile name to support multiple accounts/profiles.
    """
    if CUSTOM_SETTINGS_CLASS is None:
        raise RuntimeError(
            "Couldn't find a registered implementation of the Settings class."
        )
    filename = "settings.json" if not profile else f"settings_{profile}.json"
    return CUSTOM_SETTINGS_CLASS.from_file(SETTINGS_PATH / filename)


def save_settings(settings: Settings, profile: Optional[str] = None) -> None:
    """
    Save the given Settings object.
    Optionally takes a profile name to suppport multiple accounts/profiles.
    """
    filename = "settings.json" if not profile else f"settings_{profile}.json"
    settings.save_to_file(SETTINGS_PATH / filename)
