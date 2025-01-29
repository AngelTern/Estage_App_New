from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.separate_location_and_number import separate_location_and_number
import re


def get_image_urls(scraper, by, value):
    if not is_loaded(scraper, by, value):
        scraper.logger.warning(f"Location element not loaded: '{by}' - '{value}"'')
        return None

    try:
        image_locations = scraper.driver.find_elements(by, value)
        if image_locations:
            image_urls = [img.get_attribute('src') for img in image_locations]
            scraper.logger.info(f"Image urls loaded: {len(image_urls)}")
            return image_urls
        return None
    except WebDriverException as e:
        scraper.logger.warning(f"WebDriver exception occurred while extracting Photos: {e}")
