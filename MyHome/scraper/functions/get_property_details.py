from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.separate_location_and_number import separate_location_and_number
import re


def get_property_details(scraper, by, value, value_space, value_room, value_bedroom, value_floor):
    if not is_loaded(scraper, by, value):
        scraper.logger.warning(f"Property details elements is not loaded: '{by}' - '{value}'")
        return (None, None, None, None, None)

    try:
        property_details_element = scraper.driver.find_element(by, value)
        if property_details_element:
            space = property_details_element.find_element(by, value_space).text
            scraper.logger.info(f"Space extracted: '{space}'")
            if not space:
                scraper.logger.warning(f"Error while extracting space from property details")
                space = "N/A"

            room = property_details_element.find_element(by, value_room).text
            scraper.logger.info(f"Room count extracted: '{room}'")
            if not room:
                scraper.logger.warning(f"Error while extracting room from property details")
                room = "N/A"

            bedroom = property_details_element.find_element(by, value_bedroom).text
            if not bedroom:
                scraper.logger.warning(f"Error while extracting bedroom from property details")
                scraper.logger.info(f"Bedroom count extracted: '{bedroom}'")
                bedroom = "N/A"

            floor_full = property_details_element.find_element(by, value_floor).text
            scraper.logger.info(f"Full floor text extracted: '{floor_full}'")
            if not floor_full:
                scraper.logger.warning(f"Error while extracting floor from property details")
                floor_full = "N/A"

            if "/" in floor_full:
                floor, total_floor = floor_full.split("/")
                scraper.logger.info(f"Floor: '{floor}'; Total floor count: '{total_floor}'")
            else:
                floor = floor_full
                total_floor = "N/A"

            return space, room, bedroom, floor, total_floor

        return (None, None, None, None, None)

    except WebDriverException as e:
        scraper.logger.error(f"Webdriver exception occurred while extracting property details: {e}")
        return (None, None, None, None, None)
