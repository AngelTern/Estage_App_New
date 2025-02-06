import logging
import time
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException
)
from BasicSeleniumSetup.functions.custom_wait import custom_wait


def scroll_to_element_centered(scraper, by, value, offset=200, timeout=10, poll_frequency=0.1):
    def condition():
        try:
            scraper.logger.debug(f"[scroll_to_element_centered.condition] Locating element using ({by}, '{value}').")
            element = scraper.driver.find_element(by, value)
            element_desc = f"({by}, '{value}')"

            # Get the current vertical scroll offset.
            old_offset = scraper.driver.execute_script("return window.pageYOffset;")
            scraper.logger.info(f"[scroll_to_element_centered] Current page Y offset: {old_offset}")

            scraper.logger.info(
                f"[scroll_to_element_centered] Scrolling to center element {element_desc} with smooth behavior and offset {offset}.")
            scraper.driver.execute_script(
                """
                const element = arguments[0];
                const offset = arguments[1];
                const rect = element.getBoundingClientRect();
                const elementY = rect.top + window.pageYOffset;
                // Calculate target scroll position minus the offset.
                const targetY = elementY - offset;
                window.scrollTo({top: targetY, behavior: 'smooth'});
                """,
                element, offset
            )

            # Pause briefly to allow the scroll animation to complete.
            time.sleep(0.5)

            # Get the new scroll offset.
            new_offset = scraper.driver.execute_script("return window.pageYOffset;")
            scraper.logger.info(f"[scroll_to_element_centered] New page Y offset after scrolling: {new_offset}")

            return True
        except (NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException) as e:
            scraper.logger.error(f"[scroll_to_element_centered] Error locating or scrolling to element: {e}")
        except Exception as e:
            scraper.logger.exception(f"[scroll_to_element_centered] Unexpected error: {e}")
        return False

    scraper.logger.info(
        f"[scroll_to_element_centered] Searching for ({by}, '{value}') with a timeout of {timeout}s and poll frequency of {poll_frequency}s.")
    return custom_wait(scraper, condition_function=condition, timeout=timeout, poll_frequency=poll_frequency)
