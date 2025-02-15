import os
import sys
import time
import json
import requests
import re
import random
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from BasicSeleniumSetup.BasicSetup import BasicScraper


def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))


class SS_Scraper(BasicScraper):
    def __init__(self, url, agency_price, currency, comment="", headless=False, stop_event=None, output_dir=None):
        super().__init__(url, headless=headless)
        self.agency_price = agency_price
        self.comment = comment
        self.stop_event = stop_event
        self.output_dir = output_dir if output_dir else os.path.join(get_base_dir(), "output")
        #os.makedirs(self.output_dir, exist_ok=True)
        self.ad_id = None
        self.currency = currency

    @staticmethod
    def download_image(url, folder_name, image_name, stop_event=None):
        if stop_event and stop_event.is_set():
            return
        os.makedirs(folder_name, exist_ok=True)
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                with open(os.path.join(folder_name, image_name), 'wb') as f:
                    f.write(response.content)
        except Exception:
            pass

    @staticmethod
    def custom_wait(driver, condition_function, timeout=10, poll_frequency=0.5, stop_event=None):
        end_time = time.time() + timeout
        while True:
            if stop_event and stop_event.is_set():
                return False
            try:
                if condition_function():
                    return True
            except Exception:
                pass
            time.sleep(poll_frequency)
            if time.time() > end_time:
                break
        return False

    @staticmethod
    def extract_additional_info_updated(driver, stop_event=None):
        additional_info = {}
        try:
            if stop_event and stop_event.is_set():
                return additional_info
            container = driver.find_element(By.CLASS_NAME, "sc-1b705347-0.hoeUnZ")
            wet_point_container = container.find_elements(By.CLASS_NAME, "sc-1b705347-1.brMFse")[0]
            wet_point = wet_point_container.find_element(By.TAG_NAME, "h3").text if wet_point_container.find_elements(
                By.TAG_NAME, "h3") else 'N/A'
            additional_info["სველი წერტილი"] = wet_point
            condition_container = container.find_elements(By.CLASS_NAME, "sc-1b705347-1.brMFse")[1]
            condition = condition_container.find_element(By.TAG_NAME, "h3").text if condition_container.find_elements(
                By.TAG_NAME, "h3") else 'N/A'
            additional_info["მდგომარეობა"] = condition
            status_container = container.find_elements(By.CLASS_NAME, "sc-1b705347-1.brMFse")[2]
            status = status_container.find_element(By.TAG_NAME, "h3").text if status_container.find_elements(
                By.TAG_NAME, "h3") else 'N/A'
            additional_info["სტატუსი"] = status
        except Exception:
            pass
        return additional_info

    @staticmethod
    def extract_breadcrumbs(driver, stop_event=None):
        breadcrumbs_data = {}
        try:
            if stop_event and stop_event.is_set():
                return breadcrumbs_data
            breadcrumb_container = driver.find_element(By.CLASS_NAME, "sc-edcd5edf-20.hLHWIj")
            breadcrumb_links = breadcrumb_container.find_elements(By.TAG_NAME, "a")
            if len(breadcrumb_links) >= 3:
                breadcrumbs_data["category"] = breadcrumb_links[0].text
                breadcrumbs_data["property_type"] = breadcrumb_links[1].text
                breadcrumbs_data["transaction_type"] = breadcrumb_links[2].text
                breadcrumbs_data["ქალაქი"] = breadcrumb_links[3].text
                breadcrumbs_data["რაიონი"] = breadcrumb_links[4].text
        except Exception:
            pass
        return breadcrumbs_data

    @staticmethod
    def extract_features_info(driver, stop_event=None):
        features_info = {}
        try:
            if stop_event and stop_event.is_set():
                return features_info
            container = driver.find_element(By.CLASS_NAME, "sc-abd90df5-0")
            feature_elements = container.find_elements(By.CLASS_NAME, "sc-abd90df5-1")
            for element in feature_elements:
                if stop_event and stop_event.is_set():
                    break
                title = element.find_element(By.TAG_NAME, "h3").text if element.find_elements(By.TAG_NAME,
                                                                                              "h3") else 'N/A'
                disabled = element.get_attribute("disabled")
                value = "კი" if disabled is None else "არა"
                features_info[title] = value
        except Exception:
            pass
        return features_info

    @staticmethod
    def extract_property_details(driver, stop_event=None):
        details = {}
        try:
            if stop_event and stop_event.is_set():
                return details
            detail_container = driver.find_element(By.CLASS_NAME, "sc-479ccbe-0.iQgmTI")
            detail_elements = detail_container.find_elements(By.CLASS_NAME, "sc-479ccbe-1.fdyrTe")
            for element in detail_elements:
                if stop_event and stop_event.is_set():
                    break
                title = element.find_element(By.CLASS_NAME, "sc-6e54cb25-16.ijRIAC").text if element.find_elements(
                    By.CLASS_NAME, "sc-6e54cb25-16.ijRIAC") else 'N/A'
                value = element.find_element(By.CLASS_NAME, "sc-6e54cb25-4.kjoKdz").text if element.find_elements(
                    By.CLASS_NAME, "sc-6e54cb25-4.kjoKdz") else 'N/A'
                if title == "საერთო ფართი":
                    details["საერთო ფართი"] = value
                elif title == "ოთახი":
                    details["ოთახი"] = value
                elif title == "საძინებელი":
                    details["საძინებელი"] = value
                elif title == "სართული":
                    if "/" in value:
                        floor, total_floors = value.split("/")
                        details["სართული"] = floor.strip()
                        details["სართულიანობა"] = total_floors.strip()
                    else:
                        details["სართული"] = value
                        details["სართულიანობა"] = "N/A"
        except Exception:
            pass
        return details

    def run(self):
        self.open_page()
        if self.stop_event and self.stop_event.is_set():
            self.close_browser()
            return None

        def get_ad_id():
            nonlocal _ad_id
            id_elements = self.driver.find_elements(By.XPATH,
                                                    "//div[contains(@class, 'sc-edcd5edf-19')]/div/span[contains(text(), 'ID -')]")
            if id_elements:
                _ad_id = id_elements[0].text.split("-")[-1].strip()
                return True
            return False

        _ad_id = None
        if not self.custom_wait(self.driver, get_ad_id, stop_event=self.stop_event):
            self.close_browser()
            return None
        self.ad_id = _ad_id
        if self.stop_event and self.stop_event.is_set():
            self.close_browser()
            return None

        # Use the base class method to create the directory structure.
        self.paths = self.save_directory()

        def get_ad_title():
            nonlocal _ad_title
            elements = self.driver.find_elements(By.CLASS_NAME, "sc-6e54cb25-0.gDYjuA")
            if elements:
                _ad_title = elements[0].text
                return True
            return False

        _ad_title = None
        if not self.custom_wait(self.driver, get_ad_title, stop_event=self.stop_event):
            self.close_browser()
            return None
        ad_title = _ad_title

        def get_location():
            nonlocal _location, _number
            elements = self.driver.find_elements(By.ID, "address")
            if elements:
                location_full = elements[0].text
                match = re.search(r'(\d+\S*)$', location_full)
                if match:
                    _number = match.group(1)
                    _location = location_full[:match.start()].strip()
                else:
                    _number = '\u200B'
                    _location = location_full.strip()
                return True
            return False

        _location, _number = None, None
        if not self.custom_wait(self.driver, get_location, stop_event=self.stop_event):
            self.close_browser()
            return None
        location, number = _location, _number

        images = []

        def get_images():
            nonlocal images
            elements = self.driver.find_elements(By.CLASS_NAME, "sc-1acce1b7-10.kCJmmf")
            if elements:
                images = [img.get_attribute("src")[:-10] + ".jpg" for img in elements]
                return True
            return False

        if not self.custom_wait(self.driver, get_images, stop_event=self.stop_event):
            self.close_browser()
            return None
        images_directory = self.paths["images_folder_path"]
        for idx, img_url in enumerate(images, start=1):
            if self.stop_event and self.stop_event.is_set():
                self.close_browser()
                return None
            self.download_image(img_url, images_directory, f"{self.ad_id}_{idx}.jpg", stop_event=self.stop_event)

        owner_price = None

        def get_owner_price():
            nonlocal owner_price
            elements = self.driver.find_elements(By.ID, "price")
            if elements:
                owner_price = elements[0].text
                if self.currency in owner_price:
                    owner_price = re.sub(self.currency, "", owner_price).strip()
                    return True
            try:
                currency_change_element = self.driver.find_element(By.CSS_SELECTOR, ".currency-box")
            except Exception:
                return False
            if currency_change_element:
                currency_change_element.click()
                time.sleep(0.4)
                elements = self.driver.find_elements(By.ID, "price")
                if elements:
                    owner_price = elements[0].text
                    owner_price = re.sub(self.currency, "", owner_price).strip()
                    return True
            return False

        if not self.custom_wait(self.driver, get_owner_price, stop_event=self.stop_event):
            self.close_browser()
            return None

        def click_show_number():
            try:
                button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'ნომრის ჩვენება')]")
                button.click()
                return True
            except Exception:
                return False

        self.custom_wait(self.driver, click_show_number, stop_event=self.stop_event)

        phone_number = None

        def get_phone_number():
            nonlocal phone_number
            elements = self.driver.find_elements(By.CLASS_NAME, "sc-6e54cb25-11.kkDxQl")
            if elements:
                phone_number = elements[0].text
                return True
            return False

        self.custom_wait(self.driver, get_phone_number, stop_event=self.stop_event)

        name = None

        def get_name():
            nonlocal name
            elements = self.driver.find_elements(By.CLASS_NAME, "sc-6e54cb25-6.eaYTaN")
            if elements:
                name = elements[0].text
                return True
            return False

        if not self.custom_wait(self.driver, get_name, stop_event=self.stop_event):
            self.close_browser()
            return None

        description = None

        def get_description():
            nonlocal description
            elements = self.driver.find_elements(By.CLASS_NAME, "sc-f5b2f014-2.cpLEJS")
            if elements:
                description = elements[0].text
                return True
            else:
                return True
            return False

        if not self.custom_wait(self.driver, get_description, stop_event=self.stop_event):
            self.close_browser()
            return None
        description = description if description else ""

        additional_info = self.extract_additional_info_updated(self.driver, stop_event=self.stop_event)
        if self.stop_event and self.stop_event.is_set():
            self.close_browser()
            return None

        breadcrumbs_data = self.extract_breadcrumbs(self.driver, stop_event=self.stop_event)
        if self.stop_event and self.stop_event.is_set():
            self.close_browser()
            return None

        features_info = self.extract_features_info(self.driver, stop_event=self.stop_event)
        if self.stop_event and self.stop_event.is_set():
            self.close_browser()
            return None

        property_details = self.extract_property_details(self.driver, stop_event=self.stop_event)
        if self.stop_event and self.stop_event.is_set():
            self.close_browser()
            return None

        project_type = additional_info.get("პროექტი") if additional_info.get("პროექტი") else "არასტანდარტული"
        state = additional_info.get("მდგომარეობა")
        if state == "ძველი რემონტით":
            state = "ძველი გარემონტებული"
        elif state == "ახალი რემონტით":
            state = "ახალი გარემონტებული"
        elif state == "გარემონტებული":
            state = "ახალი გარემონტებული"
        print(state)

        additional_parameters = {
            "სტატუსი": additional_info.get("სტატუსი") if additional_info.get("სტატუსი") else None,
            "მდგომარეობა": state,
            "პროექტის ტიპი": project_type,
        }
        if additional_info.get("სველი წერტილი"):
            additional_parameters["სვ.წერტილები"] = additional_info.get("სველი წერტილი")
        if features_info.get("ცენტ. გათბობა") and features_info.get("ცენტ. გათბობა") == "კი":
            additional_parameters["გათბობა"] = "ცენტრალური გათბობა"
        if features_info.get("აივანი") and features_info.get("აივანი") == "კი":
            additional_parameters["აივანი"] = "1"
        if features_info.get("ინტერნეტი") and features_info.get("ინტერნეტი") == "კი":
            additional_parameters["ინტერნეტი"] = "კი"
        if features_info.get("საკაბელო ტელევიზია") and features_info.get("საკაბელო ტელევიზია") == "კი":
            additional_parameters["ტელევიზია"] = "კი"
        if features_info.get("ბუნებრივი აირი") and features_info.get("ბუნებრივი აირი") == "კი":
            additional_parameters["ბუნ. აირი"] = "კი"
        if features_info.get("ლიფტი") and features_info.get("ლიფტი") == "კი":
            additional_parameters["ლიფტი"] = "კი"

        furniture = []
        if features_info.get("ავეჯი") and features_info.get("ავეჯი") == "კი":
            furniture.append("ავეჯი")
        if features_info.get("სარეცხი მანქანა") and features_info.get("სარეცხი მანქანა") == "კი":
            furniture.append("სარეცხი მანქანა")

        data = {
            "ad_id": self.ad_id,
            "ad_title": ad_title,
            "location": location,
            "number": number,
            "images": images,
            "owner_price": owner_price,
            "currency": self.currency,
            "agency_price": self.agency_price,
            "phone_number": phone_number,
            "name": name,
            "description": description,
            "comment": self.comment,
            "property_details": property_details,
            "additional_info": additional_info,
            "breadcrumbs": breadcrumbs_data,
            "additional_parameters": additional_parameters,
            "furniture": furniture,
            "features": features_info,
        }
        file_path = os.path.join(self.paths["directory_path"], f"{self.ad_id}.json")
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        return self.ad_id

    def close_browser(self):
        super().close_browser()


if __name__ == "__main__":
    scraper = SS_Scraper(
        url="https://home.ss.ge/ka/udzravi-qoneba/qiravdeba-3-otaxiani-bina-vakeshi-31141042",
        agency_price="200", currency="$", comment="", headless=True
    )
    ad_id = scraper.run()
    scraper.close_browser()
    print("Scraped ad ID:", ad_id)
