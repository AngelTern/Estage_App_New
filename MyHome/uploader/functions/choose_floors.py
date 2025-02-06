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


def choose_floors(scraper, by, value_floor, value_floor_total, floor, floor_total):
    if not is_loaded(scraper, by, value_floor) or not is_loaded(scraper, by, value_floor_total):
        scraper.logger.warning(f"Choose floor and/or total floor input(s) are not loaded")
        return

    if not scroll_to_element_centered(scraper, by, value_floor):
        scraper.logger.warning(f"Could not scroll down to floor selection")
        return

    try:
        floor_number_input_element = scraper.driver.find_element(by, value_floor)
        scraper.logger.info("Floor input element found using selector '%s'", value_floor)
        if floor_number_input_element and click_element(scraper, by, value_floor):
            scraper.logger.info("Clicked on floor input element with selector '%s'", value_floor)
            if not send_keys_to_element(scraper, by, value_floor, floor):
                scraper.logger.error(f"Could not send keys '{floor}' to '{value_floor}'")
                return
            scraper.logger.info(f"Floor '{floor}' keys successfully sent to '{value_floor}'")

        total_floor_number_input_element = scraper.driver.find_element(by, value_floor)
        scraper.logger.info("Total floor input element found using selector '%s'", value_floor_total)
        if total_floor_number_input_element and click_element(scraper, by, value_floor_total):
            scraper.logger.info("Clicked on total floor input element with selector '%s'", value_floor_total)
            if not send_keys_to_element(scraper, by, value_floor_total, floor_total):
                scraper.logger.error(f"Could not send keys '{floor_total}' to '{value_floor_total}'")
                return
            scraper.logger.info(f"Total floor '{floor_total}' keys successfully sent to '{value_floor_total}'")
            return True
        return
    except WebDriverException as e:
        scraper.logger.error(f"WebDriver exception occurred while trying to"
                             f" select floor and/or total floor count: %s", e)
        return
