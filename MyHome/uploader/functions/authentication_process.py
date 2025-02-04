from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.separate_location_and_number import separate_location_and_number
from BasicSeleniumSetup.functions.click_element import click_element
from BasicSeleniumSetup.functions.send_keys_to_element import send_keys_to_element
import re


def authenticate(scraper, by, first_button, email_field, password_field, proceed_button, email_value, password_value):
    if not is_loaded(scraper, by, first_button):
        scraper.logger.warning(f"Button to move to authentication is not loaded: '{by}' '{first_button}'")
        return False

    try:
        if click_element(scraper, by, first_button):
            scraper.logger.info(f"Successfully clicked first button: '{by}' - '{first_button}'")
        else:
            scraper.logger.error(f"Failed to click first button: '{by}' - '{first_button}'")
            return False

        if not (is_loaded(scraper, by, email_field) and
                is_loaded(scraper, by, password_field) and
                is_loaded(scraper, by, proceed_button)):
            scraper.logger.warning("Email field, password field, or proceed button are not loaded")
            return False

        scraper.logger.info("Trying to input email...")
        if send_keys_to_element(scraper, by, email_field, email_value):
            scraper.logger.info(f"Successfully typed email into '{email_field}'")
        else:
            scraper.logger.error(f"Could not type email into '{email_field}'")
            return False

        scraper.logger.info("Trying to input password...")
        if send_keys_to_element(scraper, by, password_field, password_value):
            scraper.logger.info(f"Successfully typed password into '{password_field}'")
        else:
            scraper.logger.error(f"Could not type password into '{password_field}'")
            return False

        scraper.logger.info("Trying to click proceed button...")
        if click_element(scraper, by, proceed_button):
            scraper.logger.info(f"Successfully clicked proceed button: '{proceed_button}'")
            return True
        else:
            scraper.logger.error(f"Failed to click proceed button: '{proceed_button}'")
            return False

    except WebDriverException as e:
        scraper.logger.error(f"WebDriverException occurred when trying to authenticate: {e}")
        return False
