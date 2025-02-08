from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.click_element import click_element
from BasicSeleniumSetup.functions.send_keys_to_element import send_keys_to_element
from BasicSeleniumSetup.functions.scroll_to_element import scroll_to_element_centered
import re
import time


def choose_storage(scraper, by, value_input, value_select_text, value_space, value_click, storage):
    if not is_loaded(scraper, by, value_input):
        scraper.logger.warning("Storage selection element is not loaded: '%s' - '%s'", by, value_input)
        return

    if not scroll_to_element_centered(scraper, by, value_input):
        scraper.logger.warning("Could not scroll down to storage selection")
        return

    try:
        if not isinstance(storage, list):
            storage = [storage]

        storage_yes = [item for item in storage if (item or "").strip() == "კი"]
        storage_others = [item for item in storage if (item or "").strip() != "კი"]
        storage_ordered = storage_yes + storage_others

        for item in storage_ordered:
            item = (item or "").strip()
            if not item:
                continue

            if item == "კი":
                if click_element(scraper, by, value_click):
                    scraper.logger.info("Clicked on general storage selection for 'კი'")
                else:
                    scraper.logger.warning("Could not click on general storage selection for 'კი'")
                continue

            storage_type = None
            storage_size = None
            if "/" not in item and re.search(r"\d", item):
                storage_size = item
            elif "/" in item:
                parts = item.split("/")
                storage_type = parts[0].strip() or None
                if len(parts) > 1:
                    storage_size = parts[1].strip() or None
            else:
                storage_type = item

            if storage_type:
                if not click_element(scraper, by, value_input):
                    scraper.logger.error("Failed to re-click on storage selection element '%s'", value_input)
                    return None

                dropdown_elements = scraper.driver.find_elements(by, value_select_text)
                if not dropdown_elements:
                    scraper.logger.warning("No storage dropdown elements found for item: '%s'", item)
                    continue

                matched = False
                for dd_element in dropdown_elements:
                    dd_text = dd_element.text.strip()
                    if dd_text == storage_type:
                        time.sleep(0.2)
                        scraper.logger.info("Match found for storage type: '%s'", storage_type)
                        if not click_element(scraper, by, dd_element):
                            scraper.logger.error("Failed to select storage element '%s'", storage_type)
                            return
                        scraper.logger.info("Clicked matching storage type '%s'", storage_type)
                        matched = True
                        break

                if not matched:
                    scraper.logger.warning("No dropdown match for '%s'", storage_type)

            if storage_size:
                if is_loaded(scraper, by, value_space):
                    if not click_element(scraper, by, value_space):
                        scraper.logger.warning("Could not click on value_space for size '%s'", storage_size)
                    else:
                        send_keys_to_element(scraper, by, value_space, storage_size)
                        scraper.logger.info("Entered storage size '%s'", storage_size)
                else:
                    scraper.logger.warning("Storage size field not loaded for '%s'", storage_size)

        return True

    except WebDriverException as e:
        scraper.logger.error("Exception while selecting storage: %s", e)
        return
