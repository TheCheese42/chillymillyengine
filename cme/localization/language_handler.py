"""Provides a class to load and request language strings."""

from __future__ import annotations

try:
    import tomllib  # type: ignore
except ImportError:
    import tomli as tomllib

from pathlib import Path

from .. import logger

DEFAULT_LANGUAGE = "en_US"


class LangDict(dict):  # type: ignore
    langcode: str
    langs_path: Path

    """Special dictionary to handle language files."""
    def __getitem__(self, key: str) -> str:
        try:
            value = str(super().__getitem__(key))
        except KeyError:
            if self.langcode == DEFAULT_LANGUAGE:
                raise KeyError(f"Language string `{key}` does not exist.")
            logger.warning(
                f"Language string for `{key}` does not exist in "
                f"`{self.langcode}` language."
            )
            value = self.get_from_default(key)
        return value

    def get_from_default(self, key: str) -> str:
        return self.__class__.from_langcode(DEFAULT_LANGUAGE)[key]

    @classmethod
    def set_languages_path(cls, path: str | Path) -> None:
        cls.langs_path = Path(path)

    @classmethod
    def from_toml(cls, toml_str: str) -> "LangDict":
        """Create a LangDict instance from a toml string."""
        dict_ = tomllib.loads(toml_str)
        obj = cls(tomllib.loads(toml_str)["strings"])
        for key, value in dict_["meta"].items():
            setattr(obj, key, value)
        return obj

    @classmethod
    def from_file(cls, file: Path | str) -> "LangDict":
        """Create a LangDict instance from a toml file."""
        with open(file, mode="r", encoding="utf-8") as fp:
            return cls.from_toml(fp.read())

    @classmethod
    def from_langcode(cls, langcode: str) -> "LangDict":
        """Create a LangDict instance from a langcode."""
        try:
            return cls.from_file(cls.langs_path / f"{langcode}.toml")
        except AttributeError:
            raise RuntimeError(
                "Must call `set_languages_path()` before instantiating "
                "from Language code."
            )
