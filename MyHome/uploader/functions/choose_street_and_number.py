import time
import difflib
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


def choose_street_and_number(scraper, by, value_street_input, value_street_select, value_street_district,
                             value_number, street, number):
    # Replace the full word with an abbreviation and remove extra spaces
    street = re.sub("ქუჩა", "ქ.", street).strip()

    if not (is_loaded(scraper, by, value_street_input) and is_loaded(scraper, by, value_number)):
        scraper.logger.warning("Input street and/or number elements are not loaded")
        return

    if not scroll_to_element_centered(scraper, by, value_street_input):
        scraper.logger.warning(f"Could not scroll down to: {value_street_input}")
        return

    try:
        # Click on the street input and send the street name
        input_street_element = scraper.driver.find_element(by, value_street_input)
        scraper.logger.info("Input street element found")
        if input_street_element and click_element(scraper, by, value_street_input):
            if not send_keys_to_element(scraper, by, value_street_input, street):
                scraper.logger.error("Could not type street into the street input")
                return
            scraper.logger.info("Successfully typed street")
        else:
            scraper.logger.error("Failed to click on street input")
            return

        # Ensure the dropdown is loaded before proceeding
        if not is_loaded(scraper, by, value_street_select):
            scraper.logger.warning("Select street dropdown is not loaded")
            return

        select_street_dropdown_elements = scraper.driver.find_elements(by, value_street_select)
        scraper.logger.info("Select street dropdown element(s) found")

        best_match = None
        best_ratio = 0.0
        exact_found = False

        # Iterate over each dropdown element to check for an exact match first.
        # If none is found, compute the similarity ratio to choose the closest match.
        for item in select_street_dropdown_elements:
            try:
                street_inner_text = item.find_element(by, value_street_district).text.strip()
            except Exception as e:
                scraper.logger.error("Error getting text from street district element: %s", e)
                continue

            # Compare in lowercase to avoid case sensitivity issues
            if street_inner_text.lower() == street.lower():
                time.sleep(0.2)
                if not click_element(scraper, by, item):
                    scraper.logger.error("Could not click select street dropdown")
                    return
                scraper.logger.info("Clicked street dropdown with exact match")
                exact_found = True
                break
            else:
                # Compute similarity ratio; a value of 1.0 means an exact match
                ratio = difflib.SequenceMatcher(None, street.lower(), street_inner_text.lower()).ratio()
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_match = item

        # If no exact match was found, click the best matching option.
        if not exact_found:
            if best_match:
                time.sleep(0.2)
                if not click_element(scraper, by, best_match):
                    scraper.logger.error("Could not click on best matching street dropdown")
                    return
                scraper.logger.info("Clicked best matching street dropdown (similarity: %.2f)", best_ratio)
            else:
                scraper.logger.warning("No matching street dropdown found")
                return

        # Finally, find the number input and send the number value.
        input_number_element = scraper.driver.find_element(by, value_number)
        if input_number_element and click_element(scraper, by, value_number):
            if not send_keys_to_element(scraper, by, value_number, number):
                scraper.logger.error("Could not type number into the number input")
                return
            scraper.logger.info("Successfully typed number")
            return True
        else:
            scraper.logger.error("Failed to click on number input")
            return

    except WebDriverException as e:
        scraper.logger.error("WebDriver exception occurred while trying to input street and number: %s", e)
