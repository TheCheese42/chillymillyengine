# Chilly Milly Engine

Game Engine for all Chilly Milly Games

## First steps

First thing to do is to call the `init_cme` function:

```python
from cme import init_cme

init_cme(app_name="Foo")
```

### Configure logger

To setup the logging module you should configure the engine's logger:

```python
from cme.logger import configure_logger
import logging

configure_logger(level=logging.INFO, debug=True)
```

If the level is left out, it will be `logging.DEBUG` or `logging.WARNING`, depending on if the `__debug__` constant is True or not. Similarly the debug parameter defaults to said constant.
