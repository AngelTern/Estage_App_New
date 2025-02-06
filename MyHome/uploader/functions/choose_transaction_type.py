from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.separate_location_and_number import separate_location_and_number
from BasicSeleniumSetup.functions.click_element import click_element
import re


def choose_transaction_type(scraper, transaction_type, by, value, value_text):
    if not is_loaded(scraper, by, value, timeout=100):
        scraper.logger.warning(f"Choose transaction type element not found: '{by}' - '{value}'")
        return

    try:
        transaction_type_buttons = scraper.driver.find_elements(by, value)
        scraper.logger.info(f"Choose transaction type element found: '{by}' - '{value}'")
        if transaction_type_buttons:
            for button in transaction_type_buttons:
                button_text = button.find_element(by, value_text).text.strip()
                if button_text == transaction_type:
                    scraper.logger.info(f"Given transaction type {transaction_type} corresponding button found")
                    if click_element(scraper, by, button):
                        scraper.logger.info(f"Transaction type button successfully clicked:"
                                            f" '{button_text}' = '{transaction_type}'")
                        return True
                else:
                    pass
        return
    except WebDriverException as e:
        scraper.logger.error(f"WebDriver exception occurred while clicking choose transaction type button: {e}")
        return
