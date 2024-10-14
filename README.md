# Chilly Milly Engine

[![Static Analysis and Tests](https://github.com/TheCheese42/chillymillyengine/actions/workflows/lint_format_test.yml/badge.svg)](https://github.com/TheCheese42/chillymillyengine/actions/workflows/lint_format_test.yml)

Game Engine for Chilly Milly Games.

## Warning

This library build on top of an older pre-release of the python arcade library. For use with a more recent version, or even the full v3 release, cme must be updated first.

## First steps

First thing to do is to call the `init_cme` function:

```python
from cme import init_cme

init_cme(app_name="My Game")
```

The name will later be used to figure the optimal config and data directories.

### Configure logger

To setup the logging module you should configure the engine's logger:

```python
from cme.logger import configure_logger
import logging

configure_logger(level=logging.INFO, debug=True)
```

If the level is left out, it will be `logging.DEBUG` or `logging.WARNING`, depending on the `__debug__` constant. Similarly the debug parameter defaults to said constant.

## Testing

Despite having an action for testing, GitHub Actions is running headless so some functions (with the `requires_window` mark) won't run there, requiring local testing before every merge as well.
