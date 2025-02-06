import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.separate_location_and_number import separate_location_and_number
from BasicSeleniumSetup.functions.click_element import click_element
import re


def click_nav_button(scraper, by, value):
    if not is_loaded(scraper, by, value):
        scraper.logger.warning(f"Nav bar selection is not loaded: '{by}' - '{value}'")
        return

    try:
        nav_bar_element = scraper.driver.find_element(by, value)
        if nav_bar_element and click_element(scraper, by, value):
            scraper.logger.info(f"Nav bar selection has been clicked: '{value}'")
            time.sleep(0.5)
            return True
        else:
            scraper.logger.error(f"Nav bar selection could not be clicked: '{value}'")
            return False

    except WebDriverException as e:
        scraper.logger.error(f"")
        return
