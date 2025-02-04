import logging
import time
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException
)
from BasicSeleniumSetup.functions.custom_wait import custom_wait

def click_element(scraper, by, value, timeout=10, poll_frequency=0.1):

    def condition():
        try:
            if isinstance(value, str):
                scraper.logger.debug(f"[click_element.condition] Locating element using ({by}, '{value}').")
                element = scraper.driver.find_element(by, value)
                element_desc = f"({by}, '{value}')"
            else:
                element = value
                element_desc = f"WebElement {element}"

            scraper.logger.info(f"[click_element] Clicking element {element_desc}.")
            element.click()
            return True

        except (NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException) as e:
            scraper.logger.error(f"[click_element] Error interacting with element {element_desc}: {e}")
        except Exception as e:
            scraper.logger.exception(f"[click_element] Unexpected error with element {element_desc}: {e}")
        return False

    if isinstance(value, str):
        search_desc = f"({by}, '{value}')"
    else:
        search_desc = f"WebElement provided directly: {value}"

    scraper.logger.info(f"[click_element] Searching for {search_desc} with a"
                        f" timeout of {timeout}s and poll frequency of {poll_frequency}s.")
    return custom_wait(scraper, condition_function=condition, timeout=timeout, poll_frequency=poll_frequency)
