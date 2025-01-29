from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.separate_location_and_number import separate_location_and_number
from BasicSeleniumSetup.functions.click_element import click_element
import re


def check_owner_price_currency(scraper, by, value):
    """
    Checks if the owner price currency is set to "$". If not, attempts to change it.

    Args:
        scraper: The Selenium WebDriver instance with logging.
        by: Locator strategy (e.g., By.CSS_SELECTOR, By.XPATH).
        value: Locator string to identify the currency element.

    Returns:
        bool: True if currency is set to "$" (or successfully changed to it), False otherwise.
    """

    if not is_loaded(scraper, by, value):
        scraper.logger.warning(f"[check_owner_price_currency] Currency element not loaded: ({by}, '{value}').")
        return False

    try:
        owner_price_currency_element = scraper.driver.find_element(by, value)
        owner_price_currency = owner_price_currency_element.text.strip()

        if owner_price_currency == "$":
            scraper.logger.info(f"[check_owner_price_currency] Currency is already '$'.")
            return True

        scraper.logger.info(
            f"[check_owner_price_currency] Current currency: '{owner_price_currency}'. Attempting to change.")
        click_element(scraper, by, value)

        # Re-check the currency after clicking
        owner_price_currency_element = scraper.driver.find_element(by, value)
        if owner_price_currency_element.text.strip() == "$":
            scraper.logger.info("[check_owner_price_currency] Successfully changed currency to '$'.")
            return True
        else:
            scraper.logger.error("[check_owner_price_currency] Failed to change currency to '$'.")
            return False

    except (NoSuchElementException, StaleElementReferenceException) as e:
        scraper.logger.error(f"[check_owner_price_currency] Error interacting with element ({by}, '{value}'): {e}")
        return False
