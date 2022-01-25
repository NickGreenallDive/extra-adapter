from copy import deepcopy
from logging import LoggerAdapter
from typing import Any, MutableMapping


class ExtraAdapter(LoggerAdapter):
    """
    A LoggerAdapter for passing `extra` information to stdlib logging.

    This wraps a stdlib logger and folds keywords passed as extra data. This can
    then be used by the handlers and formatters, by parsing the attributes of the 
    LogRecord.

    Quickstart usage:
    >>> from extra_adapter import ExtraAdapter
        import logging
        logging.basicConfig(level=logging.INFO, format="%(misc)-8s %(message)s")
        adapter = ExtraAdapter(logging.getLogger(), {"misc": "unknown"})
        adapter.info("this is a message")
        adapter.info("this is also a message", misc="foo-bar")
    """

    PROPAGATE_KWARGS = {
        "exc_info",
        "stack_info",
        "stacklevel",
    }

    def process(self, msg: str, kwargs: MutableMapping[str, Any]):
        new_kwargs = {}
        new_kwargs["extra"] = deepcopy(self.extra) if self.extra is not None else {}
        for key, value in kwargs.items():
            if key in self.PROPAGATE_KWARGS:
                new_kwargs[key] = value
            else:
                new_kwargs["extra"][key] = value  # type: ignore
        return msg, new_kwargs
