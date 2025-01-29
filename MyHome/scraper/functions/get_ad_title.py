from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
import re


def get_ad_title(scraper, by, value):
    if not is_loaded(scraper, by, value):
        scraper.logger.warning(f"Ad Title element not loaded: '{by}' - '{value}'")
        return None

    try:
        ad_title_element = scraper.driver.find_element(by, value)
        if ad_title_element:
            ad_title = ad_title_element.text
            scraper.logger.info(f"Ad Title extracted: '{ad_title}'")
            return ad_title
        return None
    except WebDriverException as e:
        scraper.logger.error(f"WebDriver exception occurred while extracting Ad Title: {e}")
        return None
