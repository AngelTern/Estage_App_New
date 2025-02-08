from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.separate_location_and_number import separate_location_and_number
import re


def get_property_details(scraper, by, value, value_name, value_value, property_details_dict):
    if not is_loaded(scraper, by, value):
        scraper.logger.warning("Property details elements not loaded: '%s' - '%s'", by, value)
        return property_details_dict

    try:
        elements = scraper.driver.find_elements(by, value)
        if not elements:
            scraper.logger.warning("No property detail elements found for '%s' - '%s'", by, value)
            return property_details_dict

        scraper.logger.info("Found %d property detail element(s) for '%s'", len(elements), value)

        for detail in elements:
            try:
                name_el = detail.find_element(by, value_name)
                value_el = detail.find_element(by, value_value)

                if not name_el or not value_el:
                    scraper.logger.warning("Missing name/value in property detail element")
                    continue

                name_text = name_el.text.strip()
                value_text = value_el.text.strip()

                if name_text == "სართული" and "/" in value_text:
                    parts = [p.strip() for p in value_text.split("/") if p.strip()]
                    if len(parts) == 2:
                        floor_text, total_floors_text = parts
                        property_details_dict["სართული"] = floor_text
                        property_details_dict["სართულიანობა"] = total_floors_text
                        scraper.logger.info(
                            "Extracted detail '%s': '%s' -> Parsed as სართული='%s', სართულიანობა='%s'",
                            name_text, value_text, floor_text, total_floors_text
                        )
                    else:
                        property_details_dict[name_text] = value_text
                        scraper.logger.warning(
                            "Value for '%s' had a slash but could not parse properly: '%s'",
                            name_text, value_text
                        )
                else:
                    property_details_dict[name_text] = value_text
                    scraper.logger.info("Extracted detail '%s': '%s'", name_text, value_text)

            except WebDriverException as e:
                scraper.logger.error("Error while extracting detail from an element: %s", e)
                continue
        return property_details_dict

    except WebDriverException as e:
        scraper.logger.error("Webdriver exception occurred while extracting property details: %s", e)
        return property_details_dict
