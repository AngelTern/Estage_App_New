import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.separate_location_and_number import separate_location_and_number
from BasicSeleniumSetup.functions.click_element import click_element
from BasicSeleniumSetup.functions.send_keys_to_element import send_keys_to_element
from BasicSeleniumSetup.functions.scroll_to_element import scroll_to_element_centered
import re


def choose_ceiling_height(scraper, by, value_ceiling_height, ceiling_height):
    if not is_loaded(scraper, by, value_ceiling_height):
        scraper.logger.warning(f"Choose ceiling height and/or total ceiling height input(s) are not loaded")
        return False

    if not scroll_to_element_centered(scraper, by, value_ceiling_height):
        scraper.logger.warning(f"Could not scroll down to ceiling height selection")
        return False

    try:
        ceiling_height_input_element = scraper.driver.find_element(by, value_ceiling_height)
        scraper.logger.info("Ceiling height input element found using selector '%s'", value_ceiling_height)

        if ceiling_height_input_element and click_element(scraper, by, value_ceiling_height):
            scraper.logger.info("Clicked on ceiling height input element with selector '%s'", value_ceiling_height)

            if not send_keys_to_element(scraper, by, value_ceiling_height, ceiling_height):
                scraper.logger.error(f"Could not send keys '{ceiling_height}' to '{value_ceiling_height}'")
                return False
            scraper.logger.info(f"Ceiling height '{ceiling_height}' keys successfully sent to '{value_ceiling_height}'")

            return True

    except WebDriverException as e:
        scraper.logger.error("WebDriver exception occurred while trying to select ceiling height: %s", e)

    return False
