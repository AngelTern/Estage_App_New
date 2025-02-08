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


def choose_furniture(scraper, by, value_button, value_text, furniture_list):
    if not is_loaded(scraper, by, value_button):
        scraper.logger.warning("Furniture selection element is not loaded: '%s' - '%s'", by, value_button)
        return

    if not scroll_to_element_centered(scraper, by, value_button):
        scraper.logger.warning("Could not scroll to furniture selection")
        return

    try:
        furniture_elements = scraper.driver.find_elements(by, value_button)
        if not furniture_elements:
            scraper.logger.warning("No furniture elements found for '%s' - '%s'", by, value_button)
            return

        scraper.logger.info("Found %d furniture element(s) for '%s'", len(furniture_elements), value_button)

        for element in furniture_elements:
            try:
                text_el = element.find_element(by, value_text)
            except NoSuchElementException:
                scraper.logger.warning("No text element '%s' inside a furniture element", value_text)
                continue

            furniture_text = text_el.text.strip()

            if furniture_text in furniture_list:
                scraper.logger.info("Furniture '%s' found in furniture_list", furniture_text)
                if not click_element(scraper, by, element):
                    scraper.logger.error("Failed to click furniture element '%s'", furniture_text)
                    return
                scraper.logger.info("Successfully clicked furniture element '%s'", furniture_text)

        return True

    except WebDriverException as e:
        scraper.logger.error("WebDriver exception occurred while choosing furniture: %s", e)
        return
