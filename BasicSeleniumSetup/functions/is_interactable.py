from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def is_interactable(scraper, by, value, timeout=10):
    try:
        WebDriverWait(scraper.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        scraper.logger.info(f"Element located with {by}: '{value}' is interactable.")
        return True
    except TimeoutException:
        scraper.logger.warning(f"Element located with {by}: '{value}' not interactable within {timeout} seconds.")
        return False
    except WebDriverException as e:
        scraper.logger.error(f"Webdriver exception occurred for element {by}: '{value}': {e}")
        return False
