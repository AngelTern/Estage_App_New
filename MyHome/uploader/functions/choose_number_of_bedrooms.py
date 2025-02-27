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


def choose_number_of_bedrooms(scraper, by, value, value_text, bedrooms):
    scraper.logger.info("Starting choose_number_of_bedrooms with bedrooms: %s", bedrooms)
    if not is_loaded(scraper, by, value):
        scraper.logger.warning("Bedroom count selection element is not loaded: '%s' - '%s'", by, value)
        return

    if not scroll_to_element_centered(scraper, by, value):
        scraper.logger.warning(f"Could not scroll down to bedroom selection")
        return

    try:
        bedroom_selection_elements = scraper.driver.find_elements(by, value)
        scraper.logger.info("Found %d bedroom selection element(s) using selector '%s'",
                            len(bedroom_selection_elements), value)
        if bedroom_selection_elements:
            for bedroom_selection in bedroom_selection_elements:
                bedroom_inner_text = bedroom_selection.find_element(by, value_text).text.strip()
                scraper.logger.debug("Bedroom selection inner text: '%s'", bedroom_inner_text)
                if bedroom_inner_text == bedrooms:
                    time.sleep(0.2)
                    scraper.logger.info("Match found for bedroom count: '%s'", bedrooms)
                    if not click_element(scraper, by, bedroom_selection):
                        scraper.logger.error("Bedroom count selection element '%s' is not selected", bedroom_selection)
                        return
                    scraper.logger.info("Successfully clicked the matching bedroom selection element")
                    return True
            scraper.logger.warning("No bedroom selection element matched the required bedroom count: '%s'", bedrooms)
        else:
            scraper.logger.warning("No bedroom selection elements found using selector '%s'", value)
        return
    except WebDriverException as e:
        scraper.logger.error("WebDriver exception occurred while trying to select bedroom count: %s", e)
        return
