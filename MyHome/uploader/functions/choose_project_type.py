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


def choose_project(scraper, by, value_input, value_select_text, project):
    if not is_loaded(scraper, by, value_input):
        scraper.logger.warning("Project selection element is not loaded: '%s' - '%s'", by, value_input)
        return

    if not scroll_to_element_centered(scraper, by, value_input):
        scraper.logger.warning(f"Could not scroll down to project selection")
        return

    try:
        project_selection_element = scraper.driver.find_element(by, value_input)
        scraper.logger.info("Project selection element found using selector '%s'", value_input)
        if project_selection_element and click_element(scraper, by, value_input):
            scraper.logger.info("Clicked on project selection element with selector '%s'", value_input)
            project_selection_dropdown = scraper.driver.find_elements(by, value_select_text)
            scraper.logger.info("Found %d project dropdown element(s) using selector '%s'",
                                len(project_selection_dropdown), value_select_text)

            for project_element in project_selection_dropdown:
                current_text = project_element.text
                if current_text == project:
                    time.sleep(0.2)
                    scraper.logger.info("Match found for project: '%s'", project)
                    if not click_element(scraper, by, project_element):
                        scraper.logger.error("Project selection element '%s' is not selected", project)
                        return

                    scraper.logger.info("Successfully clicked the matching project element")
                    return True
            scraper.logger.warning("No project dropdown element matched the specified project: '%s'", project)
        else:
            scraper.logger.error("Failed to click on project selection element with selector '%s'", value_input)
        return None
    except WebDriverException as e:
        scraper.logger.error("WebDriver exception occurred while trying to select project: %s", e)
        return
