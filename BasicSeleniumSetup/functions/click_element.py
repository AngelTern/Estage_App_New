import logging
import time
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from BasicSeleniumSetup.functions.custom_wait import custom_wait
import time


def click_element(scraper, by, value, timeout=10, poll_frequency=0.1):
    """Attempts to click an element within a given timeout period."""

    def condition():
        try:
            element = scraper.driver.find_element(by, value)
            if element.is_displayed() and element.is_enabled():
                scraper.logger.info(f"[click_element] Clicking element ({by}, '{value}').")
                element.click()
                return True
            scraper.logger.warning(f"[click_element] Element ({by}, '{value}') is not interactable.")
        except (NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException) as e:
            scraper.logger.error(f"[click_element] Error interacting with element ({by}, '{value}'): {e}")
        return False

    scraper.logger.info(f"[click_element] Searching for ({by}, '{value}') with a timeout of {timeout}s.")
    return custom_wait(scraper, condition_function=condition, timeout=timeout, poll_frequency=poll_frequency)
