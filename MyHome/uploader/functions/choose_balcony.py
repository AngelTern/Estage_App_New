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


def choose_balcony(scraper, by, value_balcony_count, value_balcony_area, balcony):
    try:
        balcony_count, balcony_area = map(str.strip, balcony.split("/"))
        balcony_area = re.sub(r"\D", "", balcony_area)
    except ValueError:
        scraper.logger.error(f"Invalid balcony input format: '{balcony}'")
        return

    if not is_loaded(scraper, by, value_balcony_count) or not is_loaded(scraper, by, value_balcony_area):
        scraper.logger.warning(f"Choose balcony count and/or balcony area input(s) are not loaded")
        return

    if not scroll_to_element_centered(scraper, by, value_balcony_count):
        scraper.logger.warning(f"Could not scroll down to balcony selection")
        return

    try:
        balcony_count_input_element = scraper.driver.find_element(by, value_balcony_count)
        scraper.logger.info("Balcony count input element found using selector '%s'", value_balcony_count)
        if balcony_count_input_element and click_element(scraper, by, value_balcony_count):
            scraper.logger.info("Clicked on balcony count input element with selector '%s'", value_balcony_count)
            if not send_keys_to_element(scraper, by, value_balcony_count, balcony_count):
                scraper.logger.error(f"Could not send keys '{balcony_count}' to '{value_balcony_count}'")
                return
            scraper.logger.info(f"Balcony count '{balcony_count}' keys successfully sent to '{value_balcony_count}'")

        balcony_area_input_element = scraper.driver.find_element(by, value_balcony_area)
        scraper.logger.info("Balcony area input element found using selector '%s'", value_balcony_area)
        if balcony_area_input_element and click_element(scraper, by, value_balcony_area):
            scraper.logger.info("Clicked on balcony area input element with selector '%s'", value_balcony_area)
            if not send_keys_to_element(scraper, by, value_balcony_area, balcony_area):
                scraper.logger.error(f"Could not send keys '{balcony_area}' to '{value_balcony_area}'")
                return
            scraper.logger.info(f"Balcony area '{balcony_area}' keys successfully sent to '{value_balcony_area}'")
            return True
        return
    except WebDriverException as e:
        scraper.logger.error(f"WebDriver exception occurred while trying to"
                             f" select balcony count and/or balcony area: %s", e)
        return
