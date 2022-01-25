import json
import logging


class StringFormatter(logging.Formatter):
    """Render record and extra items to a human readable string."""

    def format(self, record: logging.LogRecord):
        record.msg = record.getMessage()
        dummy = logging.LogRecord(None, None, None, None, None, None, None)  # type: ignore
        record.args = tuple()
        extra_messages = "  ".join(
            [f"{k}={v}" for k, v in record.__dict__.items() if k not in dummy.__dict__]
        )
        return record.msg + " " + extra_messages


class JSONFormatter(logging.Formatter):
    """Render record and extra items to JSON format."""

    def format(self, record: logging.LogRecord):
        record.msg = record.getMessage()
        dummy = logging.LogRecord(None, None, None, None, None, None, None)  # type: ignore
        record.args = tuple()
        output = dict(message=record.msg)
        for key, value in record.__dict__.items():
            if key not in dummy.__dict__:
                output[key] = str(value)
        return json.dumps(output)
