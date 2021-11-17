from logging import LoggerAdapter


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
        "exc_info", "stack_info", "stacklevel",
    }

    def process(self, msg, kwargs):
        new_kwargs = {}
        new_kwargs["extra"] = self.extra if self.extra is not None else {}
        for k,v in kwargs.items():
            if k in self.PROPAGATE_KWARGS:
                new_kwargs[k] = v
            else:
                new_kwargs["extra"][k] = v
        return msg, new_kwargs


