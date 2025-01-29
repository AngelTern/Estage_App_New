from BasicSeleniumSetup.BasicSetup import BasicScraper
from BasicSeleniumSetup.functions.download_images import download_images
from MyHome_Scrape_Selectors import MyHomeScrapeSelectors
from functions.get_ad_id import get_ad_id
from functions.get_ad_title import get_ad_title
from functions.get_location import get_location
from functions.get_image_urls import get_image_urls
from functions.get_owner_price import get_owner_price
from functions.click_owner_number_button import click_owner_number_button
from functions.get_owner_number import get_owner_number

"""--------------------------------------------------"""
from selenium.webdriver.common.by import By


class MyHomeScraper(BasicScraper):
    def __init__(self, url, headless=True, log_file="scraper.log"):
        super().__init__(url, headless, log_file)

    def scrape_for_ad_id(self):
        self.ad_id = get_ad_id(self, By.CSS_SELECTOR, MyHomeScrapeSelectors.ID)

    def main_scrape(self):
        self.ad_title = get_ad_title(self, By.CSS_SELECTOR, MyHomeScrapeSelectors.AD_TITLE)
        self.location, self.number = get_location(self, By.CSS_SELECTOR, MyHomeScrapeSelectors.LOCATION)
        self.owner_price = get_owner_price(self, By.CSS_SELECTOR, MyHomeScrapeSelectors.OWNER_PRICE)
        if click_owner_number_button(self, By.CSS_SELECTOR, MyHomeScrapeSelectors.OWNER_NUMBER_BUTTON):
            self.owner_number = get_owner_number(self, By.CSS_SELECTOR, MyHomeScrapeSelectors.OWNER_NUMBER)

    def get_images(self):
        self.images = get_image_urls(self, By.CSS_SELECTOR, MyHomeScrapeSelectors.IMAGES)

        if not self.ad_id:
            self.logger.error("Error: Ad ID is NONE")

        if not self.images:
            self.logger.warning(f"No images found for {self.ad_id}")
            return

        paths = self.save_directory()
        images_folder_path = paths["images_folder_path"]

        for index, image_url in enumerate(self.images):
            image_name = f"image_{index + 1}.jpg"
            self.logger.info(f"Downloading image {image_name} for {self.ad_id}")
            download_images(image_url, images_folder_path, image_name)


if __name__ == '__main__':
    obj = MyHomeScraper(url="https://www.myhome.ge/pr/19855161/qiravdeba-2-otaxiani-bina-ortachalashi/",
                        headless=False)
    obj.open_page()
    obj.scrape_for_ad_id()
    obj.main_scrape()
    obj.get_images()
    obj.close_browser()
