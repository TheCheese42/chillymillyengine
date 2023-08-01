"""
Provides a class to load and request localization strings.
LangDict operates on toml files with the following, minimal format:

```toml
[meta]
langcode = <string in lang_COUNTRY format e.g. 'en_US'>

[strings]
```
"""

from .language_handler import DEFAULT_LANGUAGE, LangDict

__all__ = [
    "DEFAULT_LANGUAGE",
    "LangDict",
]
