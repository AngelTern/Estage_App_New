from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.custom_wait import custom_wait
import re

def get_owner_number(scraper, by, value):
    """Extracts the owner's number ensuring it contains exactly 12 digits but returns the original string."""

    if not is_loaded(scraper, by, value):
        scraper.logger.error(f"Owner number element not loaded: '{by}' - '{value}'")
        return None

    def condition():
        """Condition to check if the element contains exactly 12 digits, ignoring spaces and other characters."""
        try:
            element = scraper.driver.find_element(by, value)
            raw_text = element.text
            digits_only = re.sub(r"\D", "", raw_text)  # Remove all non-digit characters
            return len(digits_only) == 12  # Ensure exactly 12 digits
        except WebDriverException:
            return False

    # Use custom_wait to wait until the element contains 12 digits
    if not custom_wait(scraper.driver, condition, timeout=10):
        scraper.logger.warning(f"Timeout reached while waiting for owner number with 12 digits.")
        return None

    try:
        owner_number_element = scraper.driver.find_element(by, value)
        owner_number_text = owner_number_element.text  # Return original string
        scraper.logger.info(f"Owner number extracted: '{owner_number_text}'")
        return owner_number_text
    except WebDriverException as e:
        scraper.logger.error(f"WebDriver exception occurred while extracting owner number: {e}")
        return None
