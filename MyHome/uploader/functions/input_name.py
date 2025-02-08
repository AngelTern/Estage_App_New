from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.click_element import click_element
from BasicSeleniumSetup.functions.send_keys_to_element import send_keys_to_element
from BasicSeleniumSetup.functions.scroll_to_element import scroll_to_element_centered
import re


def input_name(scraper, by, value, name):
    if not is_loaded(scraper, by, value):
        scraper.logger.warning(f"Name input element is not loaded: '{by}' - '{value}'")
        return

    if not scroll_to_element_centered(scraper, by, value):
        scraper.logger.warning(f"Could not scroll to name input")
        return

    try:
        name_input_element = scraper.driver.find_element(by, value)
        if name_input_element:
            if not click_element(scraper, by, name_input_element):
                scraper.logger.error(f"Could not click name input element")
                return
            if not send_keys_to_element(scraper, by, name_input_element, name):
                scraper.logger.error(f"Could not send name to name input element")
                return
            scraper.logger.info(f"Name input successfully")
    except WebDriverException as e:
        scraper.logger.erro(f"Webdriver exception occurred when trying input name: {e}")
        return