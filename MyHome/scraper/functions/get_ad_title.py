from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
import re
import json

transaction_types = ["იყიდება", "ქირავდება", "გირავდება", "ქირავდება დღიურად"]
property_types = ["ბინა", "კერძო სახლი", "აგარაკი", "მიწის ნაკვეთი", "კომერციული ფართი", "სასტუმრო"]


def get_ad_title(scraper, by, value, value_script):
    scraper.logger.info("Entering get_ad_title")
    if not is_loaded(scraper, by, value):
        scraper.logger.warning("Ad Title element not loaded: %s - %s", by, value)
        return None

    try:
        ad_title_element = scraper.driver.find_element(by, value)
        if not ad_title_element:
            scraper.logger.error("Ad Title element not found")
            return None

        ad_title = ad_title_element.text.strip()

        scraper.logger.info("Ad Title extracted: %s", ad_title)

        found_transaction_types = [t for t in transaction_types if t in ad_title]
        found_property_types = [p for p in property_types if p in ad_title]

        scraper.logger.debug("Found transaction types: %s", found_transaction_types)
        scraper.logger.debug("Found property types: %s", found_property_types)

        if not found_transaction_types:
            scraper.logger.warning("No transaction type found in Ad Title")

        if not found_property_types:
            scraper.logger.warning("No property type found in Ad Title")

        if len(found_transaction_types) > 1:
            scraper.logger.warning("More than one transaction type found: %s", found_transaction_types)

        if len(found_property_types) > 1:
            scraper.logger.warning("More than one property type found: %s", found_property_types)

        transaction_type_result = found_transaction_types[0] if found_transaction_types else None
        property_type_result = found_property_types[0] if found_property_types else None
        district_result = None
        city_result = None

        script_inner_data_element = scraper.driver.find_element(by, value_script)
        if script_inner_data_element:
            script_inner_data = script_inner_data_element.get_attribute("innerHTML")
            script_inner_data_json = json.loads(script_inner_data)
            district_result = \
                script_inner_data_json["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"]["data"]["data"][
                    "statement"]["urban_name"]
            city_result = script_inner_data_json["props"]["pageProps"]["dehydratedState"]["queries"][0] \
                ["state"]["data"]["data"]["statement"]["city_name"]
            scraper.logger.info(f"Found district: '{district_result}'")
            scraper.logger.info(f"Found city: '{city_result}'")


        scraper.logger.info("Returning ad title: %s, transaction type: %s, property type: %s, district: %s",
                            ad_title, transaction_type_result, property_type_result, district_result)

        return ad_title, transaction_type_result, property_type_result, district_result, city_result
    except WebDriverException as e:
        scraper.logger.error("WebDriver exception occurred while extracting Ad Title: %s", e)
        return None
