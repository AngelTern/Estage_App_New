import time
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

hot_water_combinations = {
    "გაზის გამაცხელებელი": "გაზის გამაცხელებელი",
    "ბაკი": "ავზი",
    "დენის გამაცხელებელი": "დენის გამაცხელებელი",
    "მზის ენერგია": "მზის გამათბობელი",
    "ცხელი წყლის გარეშე": "ცხელი წყლის გარეშე",
    "ცენტრალური გათბობა": "ცენტრალური ცხელი წყალი",
    "ბუნებრივი გათბოა": "ბუნებრივი ცხელი წყალი",
    "ინდივიდუალური": "ინდივიდუალური"
}


def choose_hot_water(scraper, by, value_input, value_select_text, hot_water):
    global hot_water_combinations

    hot_water = hot_water_combinations.get(hot_water, hot_water)

    if not is_loaded(scraper, by, value_input):
        scraper.logger.warning("Hot water selection element is not loaded: '%s' - '%s'", by, value_input)
        return

    if not scroll_to_element_centered(scraper, by, value_input):
        scraper.logger.warning(f"Could not scroll down to hot water selection")
        return

    try:
        hot_water_selection_element = scraper.driver.find_element(by, value_input)
        scraper.logger.info("Hot water selection element found using selector '%s'", value_input)
        if hot_water_selection_element and click_element(scraper, by, value_input):
            scraper.logger.info("Clicked on hot water selection element with selector '%s'", value_input)
            hot_water_selection_dropdown = scraper.driver.find_elements(by, value_select_text)
            scraper.logger.info("Found %d hot water dropdown element(s) using selector '%s'",
                                len(hot_water_selection_dropdown), value_select_text)

            for hot_water_element in hot_water_selection_dropdown:
                current_text = hot_water_element.text.strip()
                if current_text == hot_water.strip():
                    time.sleep(0.2)
                    scraper.logger.info("Match found for hot water: '%s'", hot_water)
                    if not click_element(scraper, by, hot_water_element):
                        scraper.logger.error("Hot water selection element '%s' is not selected", hot_water)
                        return

                    scraper.logger.info("Successfully clicked the matching hot water element")
                    return True
            scraper.logger.warning("No hot water dropdown element matched the specified hot water: '%s'", hot_water)
        else:
            scraper.logger.error("Failed to click on hot water selection element with selector '%s'", value_input)
        return None
    except WebDriverException as e:
        scraper.logger.error("WebDriver exception occurred while trying to select hot water: %s", e)
        return
