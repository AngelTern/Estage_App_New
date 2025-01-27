from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import logging


class BasicScraper:
    def __init__(self, url, headless=True, log_file="scraper.log"):
        self.url = url
        self.headless = headless

        logging.basicConfig(filename=log_file, filemode='w', level=logging.INFO,
                            format="%(asctime)s - %(levelname)s - %(message)s")
        self.logger = logging.getLogger(__name__)

        options = Options()
        if self.headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
        try:
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            self.driver.maximize_window()
            self.logger.info(f"Webdriver initialized successfully")
        except Exception as e:
            self.logger.error(f"Error initializing chrome driver: {e}")
            self.driver = None

    def open_page(self):
        if self.driver:
            try:
                self.driver.get(self.url)
                self.logger.info(f"Successfully opened {self.url}")
            except Exception as e:
                self.logger.error(f"Error opening {self.url}: {e}")

    def close_browser(self):
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info(f"Browser successfully closed")
            except Exception as e:
                self.logger.error(f"Error closing the browser: {e}")
