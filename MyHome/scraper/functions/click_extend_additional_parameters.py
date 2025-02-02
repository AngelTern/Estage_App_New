from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.separate_location_and_number import separate_location_and_number
from BasicSeleniumSetup.functions.click_element import click_element
import re


def click_extend_additional_parameters(scraper, by, value):
    if not is_loaded(scraper, by, value):
        scraper.logger.warning(f"Extend additional parameters button element not loaded: {by} - {value}")
        return False

    try:
        if click_element(scraper, by, value):
            scraper.logger.info(f"Successfully clicked: '{by}' - '{value}'")
            return True
        return False
    except WebDriverException as e:
        scraper.logger.error(f"WebDriver exception occurred while clicking extend additional parameters button: {e}")
        return False
