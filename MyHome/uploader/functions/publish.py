import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.click_element import click_element
from BasicSeleniumSetup.functions.send_keys_to_element import send_keys_to_element
from BasicSeleniumSetup.functions.scroll_to_element import scroll_to_element_centered
import re


def publish(scraper, by, value):
    if not is_loaded(scraper, by, value):
        scraper.logger.warning(f"Publish button element is not loaded: '{by}' - '{value}'")
        return

    if not scroll_to_element_centered(scraper, by, value):
        scraper.logger.warning(f"Could not scroll to publish button")
        return

    try:
        publish_button_element = scraper.driver.find_element(by, value)
        if publish_button_element:
            if not click_element(scraper, by, value):
                scraper.logger.error(f"Could not click publish button")
                return
            scraper.logger.info(f"Successfully published")
    except WebDriverException as e:
        scraper.logger.erro(f"Webdriver exception occurred when trying to publish: {e}")
        return
