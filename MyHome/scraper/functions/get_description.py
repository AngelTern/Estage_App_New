from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.separate_location_and_number import separate_location_and_number
import re


def get_description(scraper, by, value):
    if not is_loaded(scraper, by, value):
        scraper.logger.warning(f"Description element is not loaded: '{by}' - '{value}'")
        return None

    try:
        desctiption_element = scraper.driver.find_element(by, value)
        if desctiption_element:
            description = desctiption_element.text
            scraper.logger.info(f"Description extracted: '{description}'")
            return description
        return None
    except WebDriverException as e:
        scraper.logger.error(f"Webdriver exception occurred while extracting description: {e}")
        return None
