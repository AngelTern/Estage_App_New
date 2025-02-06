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
import re


def choose_city(scraper, by, value, value_select, city_value):
    if not is_loaded(scraper, by, value, timeout=100):
        scraper.logger.warning(f"Choose city element not found: '{by}' - '{value}'")
        return

    try:
        city_input_element = scraper.driver.find_element(by, value)
        scraper.logger.info(f"Choose city input found: '{by}' - '{value}'")
        if city_input_element and click_element(scraper, by, value):
            if not send_keys_to_element(scraper, by, value, city_value):
                return
            scraper.logger.info(f"Successfully typed city")

            if not is_loaded(scraper, by, value_select, timeout=100):
                scraper.logger.warning(f"Select city dropdown element not found: '{by}' - '{value}'")
                return

            if scraper.driver.find_element(by, value_select).text.strip() == city_value:

                if click_element(scraper, by, value_select):
                    return True

        return

    except WebDriverException as e:
        scraper.logger.error(f"WebDriver exception occurred while inputting city: {e}")
        return
