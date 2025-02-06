from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.separate_location_and_number import separate_location_and_number
import re


def get_owner_price(scraper, by, value, currency_to_set):
    if not is_loaded(scraper, by, value):
        scraper.logger.warning(f"Owner price element not loaded: '{by}' - '{value}'")
        return None

    try:
        owner_price_element = scraper.driver.find_element(by, value)
        if owner_price_element:
            owner_price = owner_price_element.text
            scraper.logger.info(f"Owner price extracted: '{owner_price}'")
            return owner_price, currency_to_set
        return None
    except WebDriverException as e:
        scraper.logger.error(f"Webdriver exception occurred while extracting owner price: {e}")
        return None
