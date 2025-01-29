import logging
import time
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

#should be driver.driver (ideally change to scraper,driver)
def click_element(driver, by, value, timeout=10, poll_frequency=0.1):
    """
    Wait up to `timeout` seconds to find and click an element specified by `by` and `value`.

    Args:
        driver: Selenium WebDriver instance.
        by: Locator strategy (e.g., By.CSS_SELECTOR, By.XPATH).
        value: Locator string (e.g., "#submit", "//button[@id='login']").
        timeout (int): Maximum wait time in seconds.
        poll_frequency (float): Interval to check for element presence.

    Returns:
        bool: True if click is successful, False otherwise.
    """

    def condition():
        try:
            element = driver.find_element(by, value)
            if element.is_displayed() and element.is_enabled():
                logging.info(f"[click_element] Clicking element located by ({by}, '{value}').")
                element.click()
                return True
            logging.warning(f"[click_element] Element located by ({by}, '{value}') is not interactable.")
        except (NoSuchElementException, ElementClickInterceptedException) as e:
            logging.error(f"[click_element] Error interacting with element ({by}, '{value}'): {e}")
        return False

    logging.info(f"[click_element] Attempting to find and click ({by}, '{value}') within {timeout}s.")
    return custom_wait(driver, condition_function=condition, timeout=timeout, poll_frequency=poll_frequency)
