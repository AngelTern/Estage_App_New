import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.separate_location_and_number import separate_location_and_number
from BasicSeleniumSetup.functions.click_element import click_element
from BasicSeleniumSetup.functions.scroll_to_element import scroll_to_element_centered
from BasicSeleniumSetup.functions.send_keys_to_element import send_keys_to_element
import re


def choose_number_of_washrooms(scraper, by, value, value_text, washrooms):
    scraper.logger.info("Starting choose_number_of_washrooms with washrooms: '%s'", washrooms)
    if not is_loaded(scraper, by, value):
        scraper.logger.warning("Washroom count selection element is not loaded: '%s' - '%s'", by, value)
        return

    if not scroll_to_element_centered(scraper, by, value):
        scraper.logger.warning(f"Could not scroll down to washroom selection")
        return

    try:
        washroom_selection_element = scraper.driver.find_element(by, value)
        scraper.logger.info("Washroom selection element found using selector '%s'", value)
        if washroom_selection_element and click_element(scraper, by, value):
            scraper.logger.info("Clicked on washroom selection element with selector '%s'", value)
            washroom_selection_dropdown = scraper.driver.find_elements(by, value_text)
            scraper.logger.info("Found %d washroom dropdown element(s) using selector '%s'",
                                len(washroom_selection_dropdown), value_text)
            for washroom in washroom_selection_dropdown:
                current_text = washroom.text.strip()
                if current_text == washrooms:
                    time.sleep(0.2)
                    scraper.logger.info("Match found for washroom count: '%s'", washrooms)
                    if not click_element(scraper, by, washroom):
                        scraper.logger.error("Washroom count selection element '%s' is not selected", washroom)
                        return
                    scraper.logger.info("Successfully clicked the matching washroom element")
                    return True
            scraper.logger.warning("No washroom dropdown element matched the specified count: '%s'", washrooms)
        else:
            scraper.logger.error("Failed to click on washroom selection element with selector '%s'", value)
        return None
    except WebDriverException as e:
        scraper.logger.error("WebDriver exception occurred while trying to select washroom count: %s", e)
        return
