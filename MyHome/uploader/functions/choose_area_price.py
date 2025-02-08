from selenium.webdriver.common.by import By
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.click_element import click_element
from BasicSeleniumSetup.functions.send_keys_to_element import send_keys_to_element
from BasicSeleniumSetup.functions.scroll_to_element import scroll_to_element_centered
import time
import re


def choose_area_price(scraper, by, value_area, value_price, value_currency_gel, value_currency_usd, area, price, currency):
    if not is_loaded(scraper, by, value_area):
        scraper.logger.warning("Area and price selection elements are not loaded: '%s' - '%s'", by, value_area)
        return

    if not scroll_to_element_centered(scraper, by, value_area):
        scraper.logger.warning("Could not scroll down to area selection.")
        return

    try:
        area_numeric = re.sub(r"\D", "", area)

        area_input_element = scraper.driver.find_element(by, value_area)
        if area_input_element:
            scraper.logger.info(f"Found area input field. Inputting value: {area_numeric}")
            if not click_element(scraper, by, value_area):
                scraper.logger.error("Failed to click on area input field.")
                return
            if not send_keys_to_element(scraper, by, value_area, area_numeric):
                scraper.logger.error("Failed to send keys to area input field.")
                return

        price_input_element = scraper.driver.find_element(by, value_price)
        if price_input_element:
            scraper.logger.info(f"Found price input field. Inputting value: {price}")
            if not click_element(scraper, by, value_price):
                scraper.logger.error("Failed to click on price input field.")
                return
            if not send_keys_to_element(scraper, by, value_price, price):
                scraper.logger.error("Failed to send keys to price input field.")
                return

        currency_element = None

        if currency == "$":
            if not click_element(scraper, by, value_currency_usd):
                scraper.logger.error("Failed to select USD currency option.")
                return
            scraper.logger.info("Selected USD as currency.")
            currency_element = scraper.driver.find_element(by, value_currency_usd)
        else:
            if not click_element(scraper, by, value_currency_gel):
                scraper.logger.error("Failed to select GEL currency option.")
                return
            scraper.logger.info("Selected GEL as currency.")
            currency_element = scraper.driver.find_element(by, value_currency_gel)

        time.sleep(0.2)

        if currency_element:
            class_attribute = currency_element.get_attribute("class")
            if "luk-select-none" not in class_attribute:
                scraper.logger.error("Currency button does not have 'luk-select-none' class after clicking.")
                return

        scraper.logger.info("Successfully set area, price, and currency.")

    except Exception as e:
        scraper.logger.error(f"Exception occurred in choose_area_price: {str(e)}")
