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


def choose_parking(scraper, by, value_input, value_select_text, parking):
    if not is_loaded(scraper, by, value_input):
        scraper.logger.warning("Parking selection element is not loaded: '%s' - '%s'", by, value_input)
        return

    if not scroll_to_element_centered(scraper, by, value_input):
        scraper.logger.warning(f"Could not scroll down to parking selection")
        return

    try:
        parking_selection_element = scraper.driver.find_element(by, value_input)
        scraper.logger.info("Parking selection element found using selector '%s'", value_input)
        if parking_selection_element and click_element(scraper, by, value_input):
            scraper.logger.info("Clicked on parking selection element with selector '%s'", value_input)
            parking_selection_dropdown = scraper.driver.find_elements(by, value_select_text)
            scraper.logger.info("Found %d parking dropdown element(s) using selector '%s'",
                                len(parking_selection_dropdown), value_select_text)

            for parking_element in parking_selection_dropdown:
                current_text = parking_element.text.strip()
                if current_text == parking.strip():
                    time.sleep(0.2)
                    scraper.logger.info("Match found for parking: '%s'", parking)
                    if not click_element(scraper, by, parking_element):
                        scraper.logger.error("Parking selection element '%s' is not selected", parking)
                        return

                    scraper.logger.info("Successfully clicked the matching parking element")
                    return True
            scraper.logger.warning("No parking dropdown element matched the specified parking: '%s'", parking)
        else:
            scraper.logger.error("Failed to click on parking selection element with selector '%s'", value_input)
        return None
    except WebDriverException as e:
        scraper.logger.error("WebDriver exception occurred while trying to select parking: %s", e)
        return
