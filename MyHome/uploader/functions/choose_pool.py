from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.separate_location_and_number import separate_location_and_number
from BasicSeleniumSetup.functions.click_element import click_element
from BasicSeleniumSetup.functions.send_keys_to_element import send_keys_to_element
from BasicSeleniumSetup.functions.scroll_to_element import scroll_to_element_centered
import re
import time


def choose_pool(scraper, by, value_input, value_select_text, value_click, pool):
    if not is_loaded(scraper, by, value_input):
        scraper.logger.warning("Pool selection element is not loaded: '%s' - '%s'", by, value_input)
        return

    if not scroll_to_element_centered(scraper, by, value_input):
        scraper.logger.warning(f"Could not scroll down to pool selection")
        return

    try:
        pool_selection_element = scraper.driver.find_element(by, value_input)
        scraper.logger.info("Pool selection element found using selector '%s'", value_input)

        if not pool_selection_element or not click_element(scraper, by, value_input):
            scraper.logger.error("Failed to click on pool selection element with selector '%s'", value_input)
            return None

        scraper.logger.info("Clicked on pool selection element with selector '%s'", value_input)
        pool_selection_dropdown = scraper.driver.find_elements(by, value_select_text)
        scraper.logger.info("Found %d pool dropdown element(s) using selector '%s'",
                            len(pool_selection_dropdown), value_select_text)

        if isinstance(pool, list):
            pool_values = set(pool)

            if "კი" in pool_values and not any(x in pool_values for x in ["ღია", "დახურული"]):
                if click_element(scraper, by, value_click):
                    scraper.logger.info("Clicked on general pool selection for 'კი'")
                    return True
                return None

            if "ღია" in pool_values:
                pool = "ღია"
            elif "დახურული" in pool_values:
                pool = "დახურული"
            else:
                scraper.logger.warning("Unexpected pool values: %s", pool)
                return None

        for pool_element in pool_selection_dropdown:
            current_text = pool_element.text.strip()
            if current_text == pool.strip():
                time.sleep(0.2)
                scraper.logger.info("Match found for pool: '%s'", pool)
                if not click_element(scraper, by, pool_element):
                    scraper.logger.error("Pool selection element '%s' is not selected", pool)
                    return
                scraper.logger.info("Successfully clicked the matching pool element")
                return True

        scraper.logger.warning("No pool dropdown element matched the specified pool: '%s'", pool)
        return None

    except WebDriverException as e:
        scraper.logger.error("WebDriver exception occurred while trying to select pool: %s", e)
        return


