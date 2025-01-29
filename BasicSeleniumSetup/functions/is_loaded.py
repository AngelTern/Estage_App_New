from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


def is_loaded(scraper, by, value, timeout=10):
    try:
        WebDriverWait(scraper.driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )
        scraper.logger.info(f"Element located with {by}: '{value} is loaded'.")
        return True
    except TimeoutException:
        scraper.logger.warning(f"Element located with {by}: '{value}' not loaded within {timeout} seconds.")
        return False
    except WebDriverException as e:
        scraper.logger.error(f"Webdriver exception occurred for element {by}: '{value}: {e}'")
        return False
