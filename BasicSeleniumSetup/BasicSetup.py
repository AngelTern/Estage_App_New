import os.path

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
        self.ad_id = None
        self.ad_title = None
        self.location = None
        self.number = None
        self.images = []
        self.owner_price = None
        self.owner_price_currency = None
        self.owner_number = None

        log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(log_dir, "scraper.log")

        file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)

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

    def save_directory(self):
        """Create a directory for the ad ID and an images folder."""
        if not self.ad_id:
            self.logger.error("Cannot create directory: ad_id is None.")
            return

        # Construct the path to the sibling 'data' folder
        base_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "data")
        )
        directory_path = os.path.join(base_path, self.ad_id)

        # Create the directory for the ad ID
        os.makedirs(directory_path, exist_ok=True)
        self.logger.info(f"Directory created: {directory_path}")

        # Create an images folder inside the directory
        images_folder_path = os.path.join(directory_path, "images")
        os.makedirs(images_folder_path, exist_ok=True)
        self.logger.info(f"Images folder created: {images_folder_path}")

        return {
            "directory_path": directory_path,
            "images_folder_path": images_folder_path,
        }
