from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
import re


def get_ad_id(scraper, by, value):
    """
    Extracts ad ID if the element is properly loaded.

    Args:
        scraper: An instance of the scraper containing the WebDriver and logger.
        by: Locator strategy (e.g., By.CSS_SELECTOR).
        value: Locator value (e.g., CSS selector string).

    Returns:
        str: The extracted ad ID or None if not found.
    """
    # Check if the element is loaded
    if not is_loaded(scraper, by, value):
        scraper.logger.warning(f"Ad ID element not loaded: '{by}' - '{value}'")
        return None

    try:
        # Find the element and extract the ID
        id_element = scraper.driver.find_element(by, value)
        if id_element:
            ad_text = id_element.text
            match = re.search(r"ID:\s*(\d+)", ad_text)  # Adjust regex to match the ID format
            if match:
                scraper.logger.info(f"Extracted Ad ID: '{match.group(1)}'")
                return match.group(1)  # Return the extracted ID
        return None
    except WebDriverException as e:
        scraper.logger.error(f"WebDriver exception occurred while extracting ad ID: {e}")
        return None
