# Extra Adapter

This is a really simple package which contains a `LoggerAdapter` class. This
class packages additional keyword arguments into the `extra` dictionary.
Additionally, a convenience method to create a logger instance, as well as formatters
that can output the logger keyword arguments are provided.

## Install

Currently this project is not on PyPi but can be directly installed from the
 git repo:
```bash
pip install git+https://github.com/NickGreenallDive/extra-adapter.git
```

## Using

This is a sub class of `logging.LoggerAdapter`, so can be initialised as a
wrapper of any logger:
```python
import logging
from extra_adapter import ExtraAdapter

logging.basicConfig(level=logging.INFO, format="%(misc)s - %(message)s")
root_logger = logging.getLogger()
adapter = ExtraAdapter(root_logger, {"misc": "None"})
adapter.info("This is a message")
adapter.info("This is a message with misc info", misc="Misc")
```

This adapter wraps keyword arguments into the `extra` keyword, so the last line
is equivalent to:
```python
root_logger.info("This is a message with misc info", extra={"misc": "Misc"})
```
The corresponding `LogRecord` object gets an attribute called `misc`, which can
be used by formatters and handlers.

### Convenience method

A basic logger configuration can be applied by using the `get_logger` function, that
will return an instance of `ExtraAdapter` that wraps a logging.Logger instance:

```python
import logging
import sys
from extra_adapter import get_logger

handler = logging.StreamHandler(sys.stdout)
logger = get_logger(name="example", level=logging.INFO, handlers=[handler])
adapter.info("This is a message")
adapter.info("This is a message with misc info", misc="Misc")
```

### Formatters

The adapter can be used with any formatter, but the package provides two useful formatters:
- **StringFormatter**: Renders a log with keyword arguments in an easily human-readable string format.
- **JSONFormatter**: Renders a log with keyword arguments in JSON format.

Besides the message and keyword arguments, the log output will render a few default log keys.
Usage:
```python
import logging
import sys
from extra_adapter import StringFormatter, get_logger

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(StringFormatter())
logger = get_logger(name="example", level=logging.INFO, handlers=[handler])
adapter.info("This is a message")
adapter.info("This is a message with misc info", misc="Misc")
```

## Further Information

Read the [logging
cookbook](https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook) - It's very helpful.
