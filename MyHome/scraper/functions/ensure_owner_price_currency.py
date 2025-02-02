from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException, \
    StaleElementReferenceException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.click_element import click_element


def ensure_owner_price_currency(scraper, by, value, value_button, currency_to_set):
    """
    Ensure that the owner's price currency is set to the desired value.
    If it's not, attempt to change it by clicking the provided button element.

    Args:
        scraper: The scraper object containing the driver and logger.
        by: The Selenium locator strategy (e.g., By.ID, By.XPATH).
        value: The locator value for the currency element.
        value_button: The locator value for the button to change currency.
        currency_to_set: The desired currency value as a string.

    Returns:
        True if the currency is correctly set, False otherwise.
    """

    if not is_loaded(scraper, by, value):
        scraper.logger.warning(f"[ensure_owner_price_currency] Currency element not loaded: ({by}, '{value}').")
        return False

    try:
        # Check the current currency text
        owner_price_currency_element = scraper.driver.find_element(by, value)
        owner_price_currency_current = owner_price_currency_element.text.strip()

        if owner_price_currency_current != currency_to_set:
            scraper.logger.info(
                "[ensure_owner_price_currency] Currency different from requested. Attempting to change...")
            if click_element(scraper, by, value_button):
                try:
                    # Wait until the element's text updates to the desired currency.
                    WebDriverWait(scraper.driver, 10).until(
                        EC.text_to_be_present_in_element((by, value), currency_to_set)
                    )
                    scraper.logger.info(f"[ensure_owner_price_currency] Currency changed to '{currency_to_set}'.")
                    return True
                except TimeoutException:
                    scraper.logger.error(
                        f"[ensure_owner_price_currency] Timeout: Currency did not change to '{currency_to_set}' after clicking.")
                    return False
            else:
                scraper.logger.error("[ensure_owner_price_currency] Failed to click the currency change button.")
                return False
        else:
            scraper.logger.info(f"[ensure_owner_price_currency] Currency is already set to '{currency_to_set}'.")
            return True

    except (WebDriverException, NoSuchElementException, StaleElementReferenceException) as e:
        scraper.logger.error(
            f"[ensure_owner_price_currency] Exception occurred while checking or setting currency: {e}")
        return False
