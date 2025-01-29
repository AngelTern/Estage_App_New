from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.separate_location_and_number import separate_location_and_number
import re


def get_location(scraper, by, value):
    if not is_loaded(scraper, by, value):
        scraper.logger.warning(f"Location element not loaded: '{by}' - '{value}'")
        return None

    try:
        location_element = scraper.driver.find_element(by, value)
        if location_element:
            location_full = location_element.text
            scraper.logger.info(f"Location extracted: '{location_full}'")
            location, number = separate_location_and_number(location_full)
            scraper.logger.info(f"Location: '{location}'; Number: '{number}'")
            return location, number
        return None, None
    except WebDriverException as e:
        scraper.logger.error(f"WebDriver exception occurred while extracting Ad Location: {e}")
        return None, None

