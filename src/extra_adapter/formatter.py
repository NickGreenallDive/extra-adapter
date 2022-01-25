import json
import logging

META_KEYS = ["filename", "levelname", "name", "lineno"]
_DUMMY_RECORD = logging.LogRecord(None, None, None, None, None, None, None)  # type: ignore


def is_output_key(key: str):
    return key not in _DUMMY_RECORD.__dict__ or key in META_KEYS


class StringFormatter(logging.Formatter):
    """Render record and extra items to a human readable string.

    The formatter will output the log message followed by attributes of the
    log record that are not present in a bare LogRecord. Additionally,
    relevant log metadata is included.

    Quickstart usage:
    >>> from extra_adapter import StringFormatter
    >>> import logging
    >>> import sys
    >>> logger = logging.get_logger("logger name")
    >>> handler = logging.StreamHandler(sys.stdout)
    >>> handler.setFormatter(StringFormatter())
    >>> logger.info("this is a message")
    this is a message: filename=current_file.py  levelname=INFO  name=logger name  lineno=7
    >>> adapter.info("this is also a message", misc="foo-bar")
    this is also a message: misc=foo-bar  filename=current_file.py  \
        levelname=INFO  name=logger name  lineno=8
    """

    def format(self, record: logging.LogRecord):
        record.msg = record.getMessage()
        record.args = tuple()
        extra_messages = "  ".join(
            [f"{k}={v}" for k, v in record.__dict__.items() if is_output_key(k)]
        )
        return record.msg + ": " + extra_messages


class JSONFormatter(logging.Formatter):
    """Render record and extra items to JSON format.

    The formatter will output the log message under a "message" key,
    followed by attributes of the log record that are not present in a bare LogRecord.
    Additionally, relevant log metadata is included.

    Quickstart usage:
    >>> from extra_adapter import JSONFormatter
    >>> import logging
    >>> import sys
    >>> logger = logging.get_logger("logger name")
    >>> handler = logging.StreamHandler(sys.stdout)
    >>> handler.setFormatter(JSONFormatter())
    >>> logger.info("this is a message")
    {"message": "this is a message", "filename": "current_file.py", \
        "levelname": "INFO", "name": "logger name", "lineno": 7}
    >>> adapter.info("this is also a message", misc="foo-bar")
    {"message": "this is also a message", "misc": "foo-bar", \
        "filename": "current_file.py", "levelname": "INFO", "name": "logger name", "lineno": 8}
    """

    def format(self, record: logging.LogRecord):
        record.msg = record.getMessage()
        record.args = tuple()
        output = dict(message=record.msg)
        for key, value in record.__dict__.items():
            if is_output_key(key):
                output[key] = str(value)
        return json.dumps(output)
