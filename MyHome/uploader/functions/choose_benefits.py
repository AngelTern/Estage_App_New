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


def choose_benefits(scraper, by, value_button, value_text, additional_parameters_data):
    if not is_loaded(scraper, by, value_button):
        scraper.logger.warning("Benefits selection element is not loaded: '%s' - '%s'", by, value_button)
        return

    if not scroll_to_element_centered(scraper, by, value_button):
        scraper.logger.warning("Could not scroll down to benefits selection")
        return

    try:
        benefit_elements = scraper.driver.find_elements(by, value_button)
        if not benefit_elements:
            scraper.logger.warning("No benefit elements found for '%s' - '%s'", by, value_button)
            return

        scraper.logger.info("Found %d benefit element(s) for '%s'", len(benefit_elements), value_button)

        for element in benefit_elements:
            try:
                text_el = element.find_element(by, value_text)
            except NoSuchElementException:
                scraper.logger.warning("Could not find text element '%s' inside benefit element", value_text)
                continue

            benefit_text = text_el.text.strip()
            if benefit_text == "სპორტ დარბაზი":
                benefit_text = "სპორტდარბაზი"
            elif benefit_text == "მაყალი/გრილი":
                benefit_text = "გრილი"


            if benefit_text in additional_parameters_data:
                benefit_value = additional_parameters_data[benefit_text]
                scraper.logger.info("Benefit '%s' matched with value '%s'", benefit_text, benefit_value)

                if not click_element(scraper, by, element):
                    scraper.logger.error("Failed to click benefit element '%s'", benefit_text)
                    return

                scraper.logger.info("Successfully clicked benefit element '%s'", benefit_text)

        return True

    except WebDriverException as e:
        scraper.logger.error("WebDriver exception occurred while choosing benefits: %s", e)
        return
