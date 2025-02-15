import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.click_element import click_element
from BasicSeleniumSetup.functions.send_keys_to_element import send_keys_to_element
from BasicSeleniumSetup.functions.scroll_to_element import scroll_to_element_centered
import re


def pay(scraper, by, value_card_balance, value_balance, value_pay):
    if not is_loaded(scraper, by, value_pay):
        scraper.logger.warning(f"Payment page is not loaded")
        return

    try:
        if not click_element(scraper, by, value_card_balance):
            scraper.logger.warning(f"Could not click Card/Balance button")
            return
        time.sleep(4)
        if not click_element(scraper, by, value_balance):
            scraper.logger.warning(f"Could not click Balance button")
            return
        time.sleep(1)
        if not click_element(scraper, by, value_pay):
            scraper.logger.warning(f"Could not click Payment button")
            return
        return True
    except WebDriverException as e:
        scraper.logger.error(f"Webdriver exception occurred when trying to pay")
        return False
