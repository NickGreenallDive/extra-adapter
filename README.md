# Extra Adapter

This is a really simple package which contains a `LoggerAdapter` class. This
class packages additional keyword arguments into the `extra` dictionary.

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

### JSON logging

This can be utalized to form structured logging using custom handler or
formatters. The most common case is a desire for a JSON logger, for this I
recommend the [python-json-logger package](https://github.com/madzak/python-json-logger).

Using with this addapter:
```
import logging
from extra_adapter import ExtraAdapter
from pythonjsonlogger import jsonlogger

root_logger = logging.getLogger()

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
root_logger.addHandler(logHandler)

adapter = ExtraAdapter(root_logger, {}) # extra is no longer required here
```
Any keywords you pass to your adapter will be propagated to your JSON messages

## Further Information

Read the [logging
cookbook](https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook) - It's very helpful.
