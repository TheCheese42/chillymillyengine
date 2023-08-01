from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from cme.localization import LangDict


@pytest.fixture
def sample_files_dir() -> str:  # type: ignore
    """Provides a tempdir with files `en_US.toml` and `de_DE.toml`."""
    with TemporaryDirectory() as tempdir:
        with open(Path(tempdir) / "en_US.toml", "w", encoding="utf-8") as fp:
            fp.write(
                "[meta]\nlangcode=\"en_US\"\n[strings]\nhello=\"Hello\""
                "\nfallback=\"Fallback\""
            )
        with open(Path(tempdir) / "de_DE.toml", "w", encoding="utf-8") as fp:
            fp.write("[meta]\nlangcode=\"de_DE\"\n[strings]\nhello=\"Hallo\"")
        yield tempdir


def test_langdict_default_lang_access(sample_files_dir: str) -> None:
    LangDict.set_languages_path(sample_files_dir)
    lang_dict = LangDict.from_langcode("en_US")
    assert lang_dict["hello"] == "Hello"


def test_langdict_default_key_error(sample_files_dir: str) -> None:
    LangDict.set_languages_path(sample_files_dir)
    lang_dict = LangDict.from_langcode("en_US")
    with pytest.raises(KeyError):
        lang_dict["non-available-key"]


def test_langdict_non_default_lang_access(sample_files_dir: str) -> None:
    LangDict.set_languages_path(sample_files_dir)
    lang_dict = LangDict.from_langcode("de_DE")
    assert lang_dict["hello"] == "Hallo"


def test_langdict_non_default_fallback(sample_files_dir: str) -> None:
    LangDict.set_languages_path(sample_files_dir)
    lang_dict = LangDict.from_langcode("de_DE")
    assert lang_dict["fallback"] == "Fallback"


def test_langdict_non_default_key_error(sample_files_dir: str) -> None:
    LangDict.set_languages_path(sample_files_dir)
    lang_dict = LangDict.from_langcode("de_DE")
    with pytest.raises(KeyError):
        lang_dict["non-available-key"]
