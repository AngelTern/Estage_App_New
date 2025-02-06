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


def choose_number_of_rooms(scraper, by, value, value_text, rooms):
    if not is_loaded(scraper, by, value):
        scraper.logger.warning(f"Room count selection element is not loaded: '{by}' - '{value}'")
        return

    if not scroll_to_element_centered(scraper, by, value):
        scraper.logger.warning(f"Could not scroll down to room selection")
        return

    try:
        room_selection_elements = scraper.driver.find_elements(by, value)
        if room_selection_elements:
            for room_selection in room_selection_elements:
                room_inner_text = room_selection.find_element(by, value_text).text.strip()
                if room_inner_text == rooms:
                    time.sleep(0.2)
                    if not click_element(scraper, by, room_selection):
                        scraper.logger.error(f"Room count selection element '{room_selection}' is not selected")
                        return
                    return True
        return
    except WebDriverException as e:
        scraper.logger.error(f"WebDriver exception occurred while trying to select room count")
        return
