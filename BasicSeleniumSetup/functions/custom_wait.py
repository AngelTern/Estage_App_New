import time
from selenium import webdriver
import logging

from selenium.common import TimeoutException


def custom_wait(driver, condition_function, timeout=10, poll_frequency=0.5):
    end_time = time.time() + timeout
    while True:
        try:
            if condition_function():
                return True
        except Exception:
            logging.exception('Exception while waiting for condition function')
        time.sleep(poll_frequency)
        if time.time() > end_time:
            break
        return False
