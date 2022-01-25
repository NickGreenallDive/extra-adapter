import json
import logging
import threading

import pytest
from src.extra_adapter import JSONFormatter, get_logger


def test_log_json_concurrency(caplog: pytest.LogCaptureFixture):
    logger = get_logger("test", level=logging.INFO)
    caplog.handler.setFormatter(JSONFormatter())

    threads = [
        threading.Thread(
            target=lambda: logger.info("thread1", value="one", additional="second")
        ),
        threading.Thread(target=lambda: logger.warning("thread2", value="two")),
        threading.Thread(target=lambda: logger.debug("thread3")),
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    lines = caplog.text.split("\n")

    logs = [json.loads(line) for line in lines if line]
    assert len(logs) == 2
    for log in logs:
        if log["levelname"] == "INFO":
            assert log["value"] == "one"
            assert log["additional"] == "second"
        elif log["levelname"] == "WARNING":
            assert log["value"] == "two"
            assert "additional" not in log
        else:
            assert False, "Wrong level was logged"
