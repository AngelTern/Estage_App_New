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
import time


def choose_entrance(scraper, by, value_input, value_select_text, value_click, entrance, entrance_type=None):
    if entrance:
        if click_element(scraper, by, value_click):
            scraper.logger.info("Clicked on entrance selection element for general entrance")
        else:
            return None

    if entrance_type:
        if not is_loaded(scraper, by, value_input):
            scraper.logger.warning("Entrance type selection element is not loaded: '%s' - '%s'", by, value_input)
            return

        if not scroll_to_element_centered(scraper, by, value_input):
            scraper.logger.warning(f"Could not scroll down to entrance type selection")
            return

        try:
            entrance_selection_element = scraper.driver.find_element(by, value_input)
            scraper.logger.info("Entrance type selection element found using selector '%s'", value_input)

            if not entrance_selection_element or not click_element(scraper, by, value_input):
                scraper.logger.error("Failed to click on entrance type selection element with selector '%s'", value_input)
                return None

            scraper.logger.info("Clicked on entrance type selection element with selector '%s'", value_input)
            entrance_selection_dropdown = scraper.driver.find_elements(by, value_select_text)
            scraper.logger.info("Found %d entrance type dropdown element(s) using selector '%s'",
                                len(entrance_selection_dropdown), value_select_text)

            for entrance_element in entrance_selection_dropdown:
                current_text = entrance_element.text.strip()
                if current_text == entrance_type.strip():
                    time.sleep(0.2)
                    scraper.logger.info("Match found for entrance type: '%s'", entrance_type)
                    if not click_element(scraper, by, entrance_element):
                        scraper.logger.error("Entrance type selection element '%s' is not selected", entrance_type)
                        return
                    scraper.logger.info("Successfully clicked the matching entrance type element")
                    return True

            scraper.logger.warning("No entrance type dropdown element matched the specified entrance type: '%s'", entrance_type)
            return None

        except WebDriverException as e:
            scraper.logger.error("WebDriver exception occurred while trying to select entrance type: %s", e)
            return
