from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from BasicSeleniumSetup.functions.custom_wait import custom_wait


def send_keys_to_element(scraper, by, value, keys):
    def condition():
        element = scraper.driver.find_element(by, value)
        scraper.logger.info(f"[send_keys_to_element] Sending keys to element located by '{by}' - '{value}'")
        element.clear()
        element.send_keys(keys)
        return True

    scraper.logger.info(f"[send_keys_to_element] Attempting to send keys to {value} within 10s")
    return custom_wait(scraper, condition)
