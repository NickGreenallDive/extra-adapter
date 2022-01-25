import json
import logging
import os
import threading

import pytest
from src.extra_adapter import JSONFormatter, get_logger


@pytest.fixture()
def log_file():
    filepath = os.path.join(os.path.dirname(__file__), "info.log")
    yield filepath
    if os.path.exists(filepath):
        os.remove(filepath)


@pytest.fixture()
def log_file_handler(log_file: str):
    handler = logging.FileHandler(log_file)
    handler.setFormatter(JSONFormatter())
    yield handler
    handler.close()


def test_log_json_concurrency(log_file: str, log_file_handler: logging.FileHandler):
    logger = get_logger("test", level=logging.INFO, handlers=[log_file_handler],)

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

    with open(log_file, "r") as f:
        lines = list(f.readlines())
        f.close()

    logs = [json.loads(line) for line in lines]
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
