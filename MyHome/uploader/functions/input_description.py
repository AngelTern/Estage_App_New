from selenium.webdriver.common.by import By
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.click_element import click_element
from BasicSeleniumSetup.functions.send_keys_to_element import send_keys_to_element
from BasicSeleniumSetup.functions.scroll_to_element import scroll_to_element_centered
import time
import re


def input_description(scraper, by, value, description):
    if not is_loaded(scraper, by, value):
        scraper.logger.warning("Description input element is not loaded: '%s' - '%s'", by, value)
        return

    if not scroll_to_element_centered(scraper, by, value):
        scraper.logger.warning("Could not scroll down to Description input.")
        return

    try:
        description_input_element = scraper.driver.find_element(by, value)
        if description_input_element:
            scraper.logger.info("Found description input field. Attempting to click and type.")
            if not click_element(scraper, by, value):
                scraper.logger.error("Failed to click the description input field.")
                return
            if not send_keys_to_element(scraper, by, value, description):
                scraper.logger.error("Failed to send keys to the description input field.")
                return
            scraper.logger.info("Successfully typed description.")
        else:
            scraper.logger.error("Description input field was not found after final check.")

    except Exception as e:
        scraper.logger.error(f"Exception occurred in input_description: {str(e)}")
