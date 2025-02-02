from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.separate_location_and_number import separate_location_and_number
import re


def get_furniture(scraper, by, value, value_name, furniture_list):
    if not is_loaded(scraper, by, value):
        scraper.logger.warning(f"Furniture element not loaded: '{by}' - '{value}'")
        return None

    try:
        furniture_elements = scraper.driver.find_elements(by, value)
        if furniture_elements:

            scraper.logger.info(f"Furniture extracted, furniture count: '{len(furniture_elements)}'")

            for furniture in furniture_elements:
                furniture_name = furniture.find_element(by, value_name).text
                furniture_list.append(furniture_name)

            return furniture_list
        return None
    except WebDriverException as e:
        scraper.logger.error(f"Webdriver exception occurred while extracting furniture: {e}")
        return None
