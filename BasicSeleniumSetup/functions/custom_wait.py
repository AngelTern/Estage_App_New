import time
import logging
from selenium import webdriver
from selenium.common.exceptions import TimeoutException


def custom_wait(scraper, condition_function, timeout=100, poll_frequency=0.5):
    """Waits for a condition to be met, polling at a specified interval."""

    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            if condition_function():
                return True
        except Exception as e:
            scraper.logger.exception(f"[custom_wait] Exception while waiting for condition: {e}")
        time.sleep(poll_frequency)

    scraper.logger.warning(f"[custom_wait] Timeout of {timeout}s reached while waiting for condition.")
    return False
