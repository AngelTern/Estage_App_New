from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.separate_location_and_number import separate_location_and_number
import re


def get_owner_number(scraper, by, value):
    if not is_loaded(scraper, by, value):
        scraper.logger.error("Owner number element not loaded: '{by}' - '{value}'")
        return None

    try:
        owner_number_element = scraper.driver.find_element(by, value)
        if owner_number_element:
            owner_number = owner_number_element.text
            scraper.logger.info(f"Owner number extracted: '{owner_number}'")
            return owner_number
        return None
    except WebDriverException as e:
        scraper.logger.error(f"WebDriver exception occurred while extracting owner number: {e}")
        return None
