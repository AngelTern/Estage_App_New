import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.click_element import click_element
from BasicSeleniumSetup.functions.send_keys_to_element import send_keys_to_element
from BasicSeleniumSetup.functions.scroll_to_element import scroll_to_element_centered
import re


def additional_upload_specifications(self, by, *selectors):
    """
    Scrolls to and clicks on multiple buttons dynamically.

    :param self: The scraper instance with driver and logging.
    :param by: The locator type (e.g., By.CSS_SELECTOR, By.XPATH).
    :param selectors: Variable-length argument list containing the button selectors.
    """

    for selector in selectors:
        if not scroll_to_element_centered(self, by, selector):
            self.logger.error(f"Could not scroll to button with selector: {selector}")
            return

        try:
            button = self.driver.find_element(by, selector)
            child_span = button.find_element(By.TAG_NAME, 'span')
            if child_span:
                click_element(self, by, button)
        except NoSuchElementException:
            pass
