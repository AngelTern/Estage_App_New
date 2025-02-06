from BasicSeleniumSetup.BasicSetup import BasicScraper
from BasicSeleniumSetup.functions.download_images import download_images
from MyHome.scraper.MyHome_Scrape_Selectors import MyHomeScrapeSelectors
from MyHome.scraper.functions.get_ad_id import get_ad_id
from MyHome.scraper.functions.get_ad_title import get_ad_title
from MyHome.scraper.functions.get_location import get_location
from MyHome.scraper.functions.get_image_urls import get_image_urls
from MyHome.scraper.functions.get_owner_price import get_owner_price
from MyHome.scraper.functions.click_owner_number_button import click_owner_number_button
from MyHome.scraper.functions.get_owner_number import get_owner_number
from MyHome.scraper.functions.get_owner_name import get_owner_name
from MyHome.scraper.functions.get_description import get_description
from MyHome.scraper.functions.get_property_details import get_property_details
from MyHome.scraper.functions.get_additional_parameters import get_additional_parameters
from MyHome.scraper.functions.click_extend_additional_parameters import click_extend_additional_parameters
from MyHome.scraper.functions.get_furtniture import get_furniture
from MyHome.scraper.functions.ensure_owner_price_currency import ensure_owner_price_currency

"""--------------------------------------------------"""
from selenium.webdriver.common.by import By
import os
import json


class MyHomeScraper(BasicScraper):
    def __init__(self, url, headless=True, log_file="scraper.log"):
        super().__init__(url, headless, log_file)
        self.additional_parameters = {}
        self.furniture = []

    def scrape_for_ad_id(self):
        self.ad_id = get_ad_id(self, By.CSS_SELECTOR, MyHomeScrapeSelectors.ID)

    def main_scrape(self, currency_to_set, agency_price, comment=None):
        self.agency_price = agency_price
        self.comment = comment

        (self.ad_title, self.transaction_type, self.property_type,
         self.district, self.city) = get_ad_title(self, By.CSS_SELECTOR, MyHomeScrapeSelectors.AD_TITLE,
                                                  MyHomeScrapeSelectors.SCRIPT_INNER_DATA)

        self.location, self.number = get_location(self, By.CSS_SELECTOR, MyHomeScrapeSelectors.LOCATION)

        if ensure_owner_price_currency(self, By.CSS_SELECTOR,
                                       MyHomeScrapeSelectors.OWNER_PRICE_CURRENCY,
                                       MyHomeScrapeSelectors.CURRENCY_CHANGE_BUTTON,
                                       currency_to_set):
            self.owner_price, self.owner_price_currency = get_owner_price(self, By.CSS_SELECTOR,
                                                                          MyHomeScrapeSelectors.OWNER_PRICE,
                                                                          currency_to_set)

        if click_owner_number_button(self, By.CSS_SELECTOR, MyHomeScrapeSelectors.OWNER_NUMBER_BUTTON):
            self.owner_number = get_owner_number(self, By.CSS_SELECTOR, MyHomeScrapeSelectors.OWNER_NUMBER)

        self.owner_name = get_owner_name(self, By.CSS_SELECTOR, MyHomeScrapeSelectors.OWNER_NAME)

        self.description = get_description(self, By.CSS_SELECTOR, MyHomeScrapeSelectors.DESCRIPTION)

        self.space, self.rooms, self.bedroom, self.floor, self.total_floor = get_property_details(self,
                                                                                                  By.CSS_SELECTOR,
                                                                                                  MyHomeScrapeSelectors.PROPERTY_DETAILS,
                                                                                                  MyHomeScrapeSelectors.SPACE,
                                                                                                  MyHomeScrapeSelectors.ROOMS,
                                                                                                  MyHomeScrapeSelectors.BEDROOM,
                                                                                                  MyHomeScrapeSelectors.FLOOR)

        if click_extend_additional_parameters(self, By.CSS_SELECTOR,
                                              MyHomeScrapeSelectors.ADDITIONAL_PARAMETERS_EXTEND_BUTTON):
            self.additional_parameters = get_additional_parameters(self, By.CSS_SELECTOR,
                                                                   MyHomeScrapeSelectors.ADDITIONAL_PARAMETERS,
                                                                   MyHomeScrapeSelectors.ADDITIONAL_PARAMETER_NAME,
                                                                   MyHomeScrapeSelectors.ADDITONAL_PARAMETER_VALUE,
                                                                   self.additional_parameters)

        self.furniture = get_furniture(self, By.CSS_SELECTOR,
                                       MyHomeScrapeSelectors.FURNITURE_SELECTION, MyHomeScrapeSelectors.FURNITURE,
                                       self.furniture)

    def get_images(self):
        self.images = get_image_urls(self, By.CSS_SELECTOR, MyHomeScrapeSelectors.IMAGES)

        if not self.ad_id:
            self.logger.error("Error: Ad ID is NONE")
            return

        if not self.images:
            self.logger.warning(f"No images found for {self.ad_id}")
            return

        self.paths = self.save_directory()
        images_folder_path = self.paths["images_folder_path"]

        local_images_path = []

        for index, image_url in enumerate(self.images):
            image_name = f"image_{index + 1}.jpg"
            local_path = os.path.join(images_folder_path, image_name)
            self.logger.info(f"Downloading image {image_name} for {self.ad_id}")
            download_images(image_url, images_folder_path, image_name)
            local_images_path.append(local_path)

        self.images = local_images_path

    def save_to_json(self):

        property_details = {
            "საერთო ფართი": self.space,
            "ოთახი": self.rooms,
            "საძინებელი": self.bedroom,
            "სართული": self.floor,
            "სართულიანობა": self.total_floor,
        }

        additional_info = {
            "სველი წერტილი": self.additional_parameters.get("სვ.წერტილები") or None,
            "მდგომარეობა": self.additional_parameters.get("მდგომარეობა") or None,
            "სტატუსი": self.additional_parameters.get("სტატუსი") or None
        }

        breadcrumbs = {
            "category": self.category,
            "property_type": self.property_type,
            "transaction_type": self.transaction_type,
            "ქალაქი": self.city,
            "რაიონი": self.district
        }

        features = {
            "კონდიციონერი": "კი" if "კონდინციონერი" in self.furniture else "არა",
            "აივანი": "კი" if "აივანი" in self.additional_parameters.keys() else "არა",
            "სარდაფი": "კი" if "სათავსო" in self.additional_parameters.keys() and
                               "სარდაფი" in self.additional_parameters["სათავსო"] else "არა",
            "საკაბელო ტელევიზია": "კი" if "ტელევიზია" in self.additional_parameters.keys() else "არა",
            "ლიფტი": "კი" if "ლიფტი" in self.additional_parameters.keys() else "არა",
            "მაცივარი": "კი" if "მაცივარი" in self.furniture else "არა",
            "ავეჯი": "კი" if "ავეჯი" in self.furniture else "არა",
            "გარაჟი": "კი" if "გარაჟი" in self.description else "არა",
            "მინა-პაკეტი": "კი" if "მინა-პაკეტი" in self.description else "არა",
            "ცენტ. გათბობა": "კი" if "გათბობა" in self.additional_parameters.keys() and
                                     "ცენტრალური გათბობა" in self.additional_parameters["გათბობა"] else "არა",
            "ცხელი წყალი": "კი" if "ცხელი წყალი" in self.additional_parameters.keys() else "არა",
            "ინტერნეტი": "კი" if "ინტერნეტი" in self.additional_parameters.keys() else "არა",
            "რკინის კარი": "კი" if "რკინის კარი" in self.description else "არა",
            "ბუნებრივი აირი": "კი" if "ბუნ. აირი" in self.additional_parameters.keys() else "არა",
            "სიგნალიზაცია": "კი" if "სიგნალიზაცია" in self.additional_parameters.keys() else "არა",
            "სათავსო": "კი" if "სათავსო" in self.additional_parameters.keys() else "არა",
            "ტელეფონი": "კი" if "ტელეფონი" in self.additional_parameters.keys() else "არა",
            "ტელევიზორი": "კი" if "ტელევიზორი" in self.description or
                                  "ტელევიზია" in self.additional_parameters.keys() else "არა",
            "სარეცხი მანქანა": "კი" if "სარეცხი მანქანა" in self.furniture else "არა"
        }

        data = {
            "original_url": self.url,
            "ad_id": self.ad_id,
            "ad_title": self.ad_title,
            "location": self.location,
            "number": self.number,
            "images": self.images,
            "owner_price": self.owner_price,
            "currency": self.owner_price_currency,
            "agency_price": self.agency_price,
            "phone_number": self.owner_number,
            "name": self.owner_name,
            "description": self.description,
            "comment": self.comment,
            "property_details": property_details,
            "additional_info": additional_info,
            "breadcrumbs": breadcrumbs,
            "additional_parameters": self.additional_parameters,
            "furniture": self.furniture,
            "features": features
        }

        file_path = os.path.join(self.paths["directory_path"], f"{self.ad_id}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return True


if __name__ == '__main__':
    obj = MyHomeScraper(url="https://www.myhome.ge/pr/20190203/qiravdeba-3-otaxiani-bina-dighomi-1-9-shi/",
                        headless=False)
    obj.open_page()
    obj.scrape_for_ad_id()
    obj.main_scrape("$", "200")
    obj.get_images()
    obj.close_browser()
    obj.save_to_json()
