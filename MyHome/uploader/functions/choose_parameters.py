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


def choose_parameters(scraper, by, value_button, value_text, additional_parameters_data):
    if not is_loaded(scraper, by, value_button):
        scraper.logger.warning("Parameters selection element is not loaded: '%s' - '%s'", by, value_button)
        return

    if not scroll_to_element_centered(scraper, by, value_button):
        scraper.logger.warning("Could not scroll down to parameters selection")
        return

    try:
        param_elements = scraper.driver.find_elements(by, value_button)
        if not param_elements:
            scraper.logger.warning("No parameter elements found for '%s' - '%s'", by, value_button)
            return

        scraper.logger.info("Found %d parameter element(s) for '%s'", len(param_elements), value_button)

        for element in param_elements:
            try:
                text_el = element.find_element(by, value_text)
            except NoSuchElementException:
                scraper.logger.warning("Could not find text element '%s' inside parameter element", value_text)
                continue

            param_text = text_el.text.strip()
            if param_text == "ბუნებრივი აირი":
                param_text = "ბუნ. აირი"
            elif param_text == "ელექტროენერგია":
                param_text = "ელ.ენერგია"
            elif param_text == "სატვირთო ლიფტი":
                param_text = "სატვ. ლიფტი"
            
            if param_text in additional_parameters_data:
                param_value = additional_parameters_data[param_text]
                scraper.logger.info("Parameter '%s' matched with value '%s'", param_text, param_value)

                if not click_element(scraper, by, element):
                    scraper.logger.error("Failed to click parameter element '%s'", param_text)
                    return

                scraper.logger.info("Successfully clicked parameter element '%s'", param_text)

        return True

    except WebDriverException as e:
        scraper.logger.error("WebDriver exception occurred while choosing parameters: %s", e)
        return
