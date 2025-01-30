from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.separate_location_and_number import separate_location_and_number
import re


def get_owner_name(scraper, by, value):
    if not is_loaded(scraper, by, value):
        scraper.logger.warning(f"Owner number element is not loaded: '{by}' - '{value}'")
        return None

    try:
        owner_name_element = scraper.driver.find_element(by, value)
        if owner_name_element:
            owner_name = owner_name_element.text
            scraper.logger.info(f"Owner name extracted: '{owner_name}'")
            return owner_name
        return None
    except WebDriverException as e:
        scraper.logger.error(f"Webdriver exception occurred while extracting owner name: {e}")
        return None
