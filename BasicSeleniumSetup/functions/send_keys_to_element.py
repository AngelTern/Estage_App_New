from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from BasicSeleniumSetup.functions.custom_wait import custom_wait
from selenium.webdriver.remote.webelement import WebElement


def send_keys_to_element(scraper, by, value, keys):
    def condition():
        if isinstance(value, WebElement):
            element = value
        else:
            element = scraper.driver.find_element(by, value)

        scraper.logger.info(f"[send_keys_to_element] Sending keys to element: {element}")
        element.clear()
        element.send_keys(keys)
        return True

    scraper.logger.info("[send_keys_to_element] Attempting to send keys within 10s")
    return custom_wait(scraper, condition)
