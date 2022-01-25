import logging
from typing import Any, Dict, List

from .adapter import ExtraAdapter
from .formatter import JSONFormatter, StringFormatter


def get_logger(
    name: str,
    level: int = logging.INFO,
    default_extra: Dict[str, Any] = None,
    handlers: List[logging.Handler] = None,
) -> ExtraAdapter:
    """Return an instance of a logger wrapped by ExtraAdapter.

    This allows keyword arguments to be passed to the LogRecord that will
    be written to the extra dictionary. Given an appropriate formatter, the
    logger will output the keyword arguments.

    Args:
        name: Logger name. Two calls with the same name will return the same log instance.
        level: Log level. Defaults to logging.INFO.
        default_extra: Extra arguments that will be included in every log call. Defaults to None.
        handlers: List of log handlers. Defaults to None.

    Returns:
        ExtraAdapter
    """
    logger = logging.getLogger(name)

    if handlers is None:
        handlers = []
    for handler in handlers:
        logger.addHandler(handler)
    logger.setLevel(level)

    return ExtraAdapter(logger, default_extra if default_extra is not None else {})
