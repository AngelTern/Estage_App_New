from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.click_element import click_element
from BasicSeleniumSetup.functions.send_keys_to_element import send_keys_to_element
from BasicSeleniumSetup.functions.scroll_to_element import scroll_to_element_centered
import re
import time


def collect_url(scraper, by, value_button, value_input, value_select, value_url):
    if not is_loaded(scraper, by, value_button):
        scraper.logger.warning("Status button not loaded.")
        return None

    try:
        profile_button = scraper.driver.find_element(by, value_button)
        if profile_button:
            if not click_element(scraper, by, value_button):
                scraper.logger.error("Failed to click the status button.")
                return None

        if not is_loaded(scraper, by, value_input, timeout=20):
            scraper.logger.warning("Input element not loaded.")
            return None

        if not click_element(scraper, by, value_input):
            scraper.logger.error("Failed to click the input element.")
            return None

        if not click_element(scraper, by, value_select):
            scraper.logger.error("Failed to click the select element.")
            return None

        element = scraper.driver.find_element(by, value_url)
        new_url = element.get_attribute('href') if element else None
        if not new_url:
            scraper.logger.error("No URL found on the element.")
        return new_url

    except WebDriverException as e:
        scraper.logger.error(f"WebDriverException occurred: {e}")
        return None

