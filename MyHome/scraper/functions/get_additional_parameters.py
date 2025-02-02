from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.separate_location_and_number import separate_location_and_number
import re


def get_additional_parameters(scraper, by, value, value_param_name, value_param_value,
                              additional_param_dict):
    if not is_loaded(scraper, by, value):
        scraper.logger.warning(f"Additional parameters element is not loaded: '{by}' - '{value}'")
        return

    try:
        additional_parameters_elements = scraper.driver.find_elements(by, value)

        if additional_parameters_elements:

            scraper.logger.info(
                f"Additional parameters extracted, parameter count: '{len(additional_parameters_elements)}'")
            for seperate_element in additional_parameters_elements:
                parameter_name = seperate_element.find_element(by, value_param_name).text
                parameter_value = seperate_element.find_element(by, value_param_value).text
                #scraper.logger.info(f"Extracted: '{parameter_name}' - '{parameter_value}'")
                additional_param_dict[parameter_name] = parameter_value
            return additional_param_dict
        return None
    except WebDriverException as e:
        scraper.logger.error(f"Webdriver exception occurred while extracting additional parameters: {e}")
        return None
