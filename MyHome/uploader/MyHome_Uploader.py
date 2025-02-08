from BasicSeleniumSetup.BasicSetup import BasicScraper
from MyHome.uploader.MyHome_Upload_Selectors import MyHomeUploadSelectors
from MyHome.uploader.functions.authentication_process import authenticate
from MyHome.uploader.functions.choose_property_type import choose_property_type
from MyHome.uploader.functions.choose_transaction_type import choose_transaction_type
from MyHome.uploader.functions.choose_city import choose_city
from MyHome.uploader.functions.choose_street_and_number import choose_street_and_number
from MyHome.uploader.functions.click_nav_button import click_nav_button
from MyHome.uploader.functions.choose_number_of_rooms import choose_number_of_rooms
from MyHome.uploader.functions.choose_number_of_bedrooms import choose_number_of_bedrooms
from MyHome.uploader.functions.choose_number_of_washrooms import choose_number_of_washrooms
from MyHome.uploader.functions.choose_floors import choose_floors
from MyHome.uploader.functions.choose_status import choose_status
from MyHome.uploader.functions.choose_state import choose_state
from MyHome.uploader.functions.choose_project_type import choose_project
from MyHome.uploader.functions.choose_ceiling_height import choose_ceiling_height
from MyHome.uploader.functions.choose_heating import choose_heating
from MyHome.uploader.functions.choose_buil_date import choose_build_date
from MyHome.uploader.functions.choose_parking import choose_parking
from MyHome.uploader.functions.choose_hot_water import choose_hot_water
from MyHome.uploader.functions.choose_balcony import choose_balcony
from MyHome.uploader.functions.choose_pool import choose_pool
from MyHome.uploader.functions.choose_entrance import choose_entrance
from MyHome.uploader.functions.choose_living_room import choose_living_room
from MyHome.uploader.functions.choose_veranda import choose_veranda
from MyHome.uploader.functions.choose_storage import choose_storage
from MyHome.uploader.functions.choose_parameters import choose_parameters
from MyHome.uploader.functions.choose_benefits import choose_benefits
from MyHome.uploader.functions.choose_furniture import choose_furniture
from MyHome.uploader.functions.choose_area_price import choose_area_price
from MyHome.uploader.functions.input_description import input_description
from MyHome.uploader.functions.upload_images import upload_images
from MyHome.uploader.functions.additional_upload_specifications import additional_upload_specifications
from MyHome.uploader.functions.publish import publish
from MyHome.uploader.functions.input_name import input_name

"""--------------------------------------------------"""

from selenium.webdriver.common.by import By
import os
import json
import time


class MyHomeUploader(BasicScraper):
    def __init__(self, url, headless=True, log_file="scraper.log"):
        super().__init__(url, headless, log_file)
        self.data = None
        self.myhome_authentication_data = None

    def primary_authenticate(self):
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "confidential"))
        print(base_path)
        json_file_path = os.path.join(base_path, "config.json")
        print(json_file_path)
        try:
            with open(json_file_path, "r", encoding="utf-8") as f:
                self.myhome_authentication_data = json.load(f)
                return self.myhome_authentication_data
        except FileNotFoundError:
            return

    def main_upload(self):
        authenticate(self, By.CSS_SELECTOR, MyHomeUploadSelectors.AUTHENTICATION_BUTTON,
                     MyHomeUploadSelectors.EMAIL_INPUT_FIELD, MyHomeUploadSelectors.PASSWORD_INPUT_FIELD,
                     MyHomeUploadSelectors.CONFIRM_AUTHENTICATION_BUTTON,
                     self.myhome_authentication_data["MyHome"]["email"],
                     self.myhome_authentication_data["MyHome"]["password"])

        choose_property_type(self, self.data["breadcrumbs"]["property_type"], By.CSS_SELECTOR,
                             MyHomeUploadSelectors.PROPERTY_TYPE_BUTTONS,
                             MyHomeUploadSelectors.PROPERTY_TYPE_TEXT)

        choose_transaction_type(self, self.data["breadcrumbs"]["transaction_type"], By.CSS_SELECTOR,
                                MyHomeUploadSelectors.TRANSACTION_TYPE_BUTTONS,
                                MyHomeUploadSelectors.TRANSACTION_TYPE_TEXT)

        choose_city(self, By.CSS_SELECTOR, MyHomeUploadSelectors.INPUT_CITY, MyHomeUploadSelectors.SELECT_CITY,
                    self.data["breadcrumbs"]["ქალაქი"])

        if self.data["breadcrumbs"].get("transaction_type") == "ყიდვა":
            choose_street_and_number(self, By.CSS_SELECTOR,
                                     MyHomeUploadSelectors.INPUT_STREET_BUY,
                                     MyHomeUploadSelectors.SELECT_STREET_BUY,
                                     MyHomeUploadSelectors.STREET_INNER_EXACT_STREET,
                                     MyHomeUploadSelectors.INPUT_STREET_NUMBER_BUY,
                                     self.data["location"],
                                     self.data["number"],
                                     self.data["breadcrumbs"]["რაიონი"])
        else:
            choose_street_and_number(self, By.CSS_SELECTOR,
                                     MyHomeUploadSelectors.INPUT_STREET,
                                     MyHomeUploadSelectors.SELECT_STREET,
                                     MyHomeUploadSelectors.STREET_INNER_EXACT_STREET,
                                     MyHomeUploadSelectors.INPUT_STREET_NUMBER,
                                     self.data["location"],
                                     self.data["number"],
                                     self.data["breadcrumbs"]["რაიონი"])

        choose_number_of_rooms(self, By.CSS_SELECTOR,
                               MyHomeUploadSelectors.ROOM_SELECTION,
                               MyHomeUploadSelectors.ROOM_SELECTION_INNER_TEXT,
                               self.data["property_details"]["ოთახი"])

        if self.data["property_details"].get("საძინებელი"):
            choose_number_of_bedrooms(self, By.CSS_SELECTOR,
                                      MyHomeUploadSelectors.BEDROOM_SELECTION,
                                      MyHomeUploadSelectors.BEDROOM_SELECTION_INNER_TEXT,
                                      self.data["property_details"]["საძინებელი"])

        if self.data["additional_parameters"].get("სვ.წერტილები"):
            choose_number_of_washrooms(self, By.CSS_SELECTOR,
                                       MyHomeUploadSelectors.WASHROOM_INPUT,
                                       MyHomeUploadSelectors.WASHROOM_DROPDOWN_SELECTION,
                                       self.data["additional_parameters"].get("სვ.წერტილები"))

        choose_floors(self, By.CSS_SELECTOR,
                      MyHomeUploadSelectors.FLOOR_INPUT,
                      MyHomeUploadSelectors.TOTAL_FLOOR_INPUT,
                      self.data["property_details"]["სართული"],
                      self.data["property_details"]["სართულიანობა"])

        choose_status(self, By.CSS_SELECTOR,
                      MyHomeUploadSelectors.STATUS_INPUT,
                      MyHomeUploadSelectors.STATUS_SELECT,
                      self.data["additional_info"]["სტატუსი"])

        if self.data["additional_parameters"].get("აშენების წელი"):
            choose_build_date(self, By.CSS_SELECTOR,
                              MyHomeUploadSelectors.BUILD_DATE_INPUT,
                              MyHomeUploadSelectors.BUILD_DATE_SELECT,
                              self.data["additional_parameters"].get("აშენების წელი"))

        if self.data["additional_info"].get("მდგომარეობა"):
            choose_state(self, By.CSS_SELECTOR,
                         MyHomeUploadSelectors.STATE_INPUT,
                         MyHomeUploadSelectors.STATE_SELECT,
                         self.data["additional_info"].get("მდგომარეობა"))

        choose_project(self, By.CSS_SELECTOR,
                       MyHomeUploadSelectors.PROJECT_INPUT,
                       MyHomeUploadSelectors.PROJECT_SELECT,
                       self.data["additional_parameters"].get("პროექტის ტიპი"))

        if self.data["additional_parameters"].get("ჭერის სიმაღლე"):
            choose_ceiling_height(self, By.CSS_SELECTOR,
                                  MyHomeUploadSelectors.CEILING_HEIGHT_INPUT,
                                  self.data["additional_parameters"].get("ჭერის სიმაღლე"))

        if self.data["additional_parameters"].get("გათბობა"):
            choose_heating(self, By.CSS_SELECTOR,
                           MyHomeUploadSelectors.HEATING_INPUT,
                           MyHomeUploadSelectors.HEATING_SELECT,
                           self.data["additional_parameters"].get("გათბობა"))

        if self.data["additional_parameters"].get("პარკირება"):
            choose_parking(self, By.CSS_SELECTOR,
                           MyHomeUploadSelectors.PARKING_INPUT,
                           MyHomeUploadSelectors.PARKING_SELECTION,
                           self.data["additional_parameters"].get("პარკირება"))

        if self.data["additional_parameters"].get("ცხელი წყალი"):
            choose_hot_water(self, By.CSS_SELECTOR,
                             MyHomeUploadSelectors.HOT_WATER_INPUT,
                             MyHomeUploadSelectors.HOT_WATER_SELECTION,
                             self.data["additional_parameters"].get("ცხელი წყალი"))

        # სამშენებლო მასალას არავინ არ ტვირთავს მაინც

        if self.data["additional_parameters"].get("აივანი"):
            choose_balcony(self, By.CSS_SELECTOR,
                           MyHomeUploadSelectors.BALCONY_COUNT_INPUT,
                           MyHomeUploadSelectors.BALCONY_AREA_INPUT,
                           self.data["additional_parameters"].get("აივანი"))

        if self.data["additional_parameters"].get("აუზი"):
            choose_pool(self, By.CSS_SELECTOR,
                        MyHomeUploadSelectors.POOL_INPUT,
                        MyHomeUploadSelectors.POOL_SELECT,
                        MyHomeUploadSelectors.POOL_CLICK,
                        self.data["additional_parameters"]["აუზი"])

        if self.data["additional_parameters"].get("მისაღები ოთახი"):
            choose_entrance(self, By.CSS_SELECTOR,
                            MyHomeUploadSelectors.ENTRANCE_INPUT,
                            MyHomeUploadSelectors.ENTRANCE_SELECT,
                            MyHomeUploadSelectors.ENTRANCE_CLICK,
                            self.data["additional_parameters"].get("მისაღები ოთახი"),
                            self.data["additional_parameters"].get("მისაღები"),)

        if self.data["additional_parameters"].get("ლოჯია"):
            choose_living_room(self, By.CSS_SELECTOR,
                               MyHomeUploadSelectors.LIVING_ROOM_CLICK,
                               self.data["additional_parameters"].get("ლოჯია"))

        if self.data["additional_parameters"].get("ვერანდა"):
            choose_veranda(self, By.CSS_SELECTOR,
                           MyHomeUploadSelectors.VERANDA_CLICK,
                           self.data["additional_parameters"].get("ვერანდა"))

        if self.data["additional_parameters"].get("სათავსო"):
            choose_storage(self, By.CSS_SELECTOR,
                           MyHomeUploadSelectors.STORAGE_INPUT,
                           MyHomeUploadSelectors.STORAGE_SELECT,
                           MyHomeUploadSelectors.STORAGE_SPACE,
                           MyHomeUploadSelectors.STORAGE_CLICK,
                           self.data["additional_parameters"].get("სათავსო"))

        choose_parameters(self, By.CSS_SELECTOR,
                          MyHomeUploadSelectors.PARAMETERS_BUTTON,
                          MyHomeUploadSelectors.PARAMETERS_BUTTON_TEXT,
                          self.data["additional_parameters"])

        choose_benefits(self, By.CSS_SELECTOR,
                        MyHomeUploadSelectors.BENEFITS_BUTTON,
                        MyHomeUploadSelectors.BENEFITS_TEXT,
                        self.data["additional_parameters"])

        choose_furniture(self, By.CSS_SELECTOR,
                         MyHomeUploadSelectors.FURNITURE_BUTTON,
                         MyHomeUploadSelectors.FURNITURE_TEXT,
                         self.data["furniture"])

        choose_area_price(self, By.CSS_SELECTOR,
                          MyHomeUploadSelectors.AREA_INPUT,
                          MyHomeUploadSelectors.PRICE_INPUT,
                          MyHomeUploadSelectors.CURRENCY_BUTTON_GEL,
                          MyHomeUploadSelectors.CURRENCY_BUTTON_USD,
                          self.data["property_details"].get("საერთო ფართი"),
                          self.data["owner_price"],
                          self.data["currency"])

        input_name(self, By.CSS_SELECTOR,
                   MyHomeUploadSelectors.NAME_INPUT,
                   self.myhome_authentication_data["MyHome"]["name"])

        input_description(self, By.CSS_SELECTOR,
                          MyHomeUploadSelectors.DESCRIPTION_INPUT,
                          self.data["description"])

        upload_images(self, By.CSS_SELECTOR,
                      MyHomeUploadSelectors.IMAGES_INPUT,
                      MyHomeUploadSelectors.IMAGES_INPUT_AFTER,
                      MyHomeUploadSelectors.IMAGES_DIV,
                      self.images_path)
        time.sleep(0.5)



    def additional_upload(self, livo, livo_vip, livo_vip_time,
                          livo_facebook, livo_facebook_time,
                          myhome_supervip, myhome_supervip_time,
                          myhome_vipplus, myhome_vipplus_time,
                          myhome_vip, myhome_vip_time,
                          add_color, add_color_time,
                          automate, automate_time_day, automate_time_hour):

        additional_upload_specifications(self, By.CSS_SELECTOR,
                                         MyHomeUploadSelectors.VALUE_LIVO, livo,
                                         MyHomeUploadSelectors.VALUE_LIVO_VIP,
                                         MyHomeUploadSelectors.VALUE_LIVO_VIP_INPUT,
                                         MyHomeUploadSelectors.VALUE_LIVO_VIP_SELECT, livo_vip, livo_vip_time,
                                         MyHomeUploadSelectors.VALUE_LIVO_FACEBOOK,
                                         MyHomeUploadSelectors.VALUE_LIVO_FACEBOOK_INPUT,
                                         MyHomeUploadSelectors.VALUE_LIVO_FACEBOOK_SELECT, livo_facebook,
                                         livo_facebook_time,
                                         MyHomeUploadSelectors.VALUE_MYHOME_SUPER_VIP,
                                         MyHomeUploadSelectors.VALUE_MYHOME_SUPER_VIP_INPUT,
                                         MyHomeUploadSelectors.VALUE_MYHOME_SUPER_VIP_SELECT, myhome_supervip,
                                         myhome_supervip_time,
                                         MyHomeUploadSelectors.VALUE_MYHOME_VIP_PLUS,
                                         MyHomeUploadSelectors.VALUE_MYHOME_VIP_PLUS_INPUT,
                                         MyHomeUploadSelectors.VALUE_MYHOME_VIP_PLUS_SELECT, myhome_vipplus,
                                         myhome_vipplus_time,
                                         MyHomeUploadSelectors.VALUE_MYHOME_VIP,
                                         MyHomeUploadSelectors.VALUE_MYHOME_VIP_INPUT,
                                         MyHomeUploadSelectors.VALUE_MYHOME_VIP_SELECT, myhome_vip, myhome_vip_time,
                                         MyHomeUploadSelectors.VALUE_ADD_COLOR,
                                         MyHomeUploadSelectors.VALUE_ADD_COLOR_INPUT,
                                         MyHomeUploadSelectors.VALUE_ADD_COLOR_SELECT, add_color, add_color_time,
                                         MyHomeUploadSelectors.VALUE_AUTOMATE,
                                         MyHomeUploadSelectors.VALUE_AUTOMATE_TIME_DAY_INPUT,
                                         MyHomeUploadSelectors.VALUE_AUTOMATE_TIME_DAY_SELECT,
                                         MyHomeUploadSelectors.VALUE_AUTOMATE_TIME_HOUR_INPUT,
                                         MyHomeUploadSelectors.VALUE_AUTOMATE_TIME_HOUR_SELECT, automate,
                                         automate_time_day, automate_time_hour)

    def finish_upload(self):
        time.sleep(5)
        publish(self, By.CSS_SELECTOR,
                MyHomeUploadSelectors.PUBLISH_BUTTON)
        time.sleep(5)

    def load_data_json(self, ad_id):
        self.ad_id = ad_id
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
        directory_path = os.path.join(base_path, self.ad_id)
        json_file_path = os.path.join(directory_path, f"{self.ad_id}.json")
        self.logger.info("%s json file located at: %s\nLoading %s.json file", self.ad_id, json_file_path, self.ad_id)
        try:
            with open(json_file_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
                self.logger.info("Successfully loaded %s.json file", self.ad_id)
                return self.data
        except FileNotFoundError as e:
            self.logger.error("%s json file not found: %s", self.ad_id, e)
        except json.decoder.JSONDecodeError as e:
            self.logger.error("%s json file is invalid: %s", self.ad_id, e)
        except PermissionError as e:
            self.logger.error("%s Permission denied while opening the file: %s", self.ad_id, e)
        except (IOError, OSError) as e:
            self.logger.error("%s Can't open or read file: %s", self.ad_id, e)
        except UnicodeError as e:
            self.logger.error("%s Encoding error while reading the file: %s", self.ad_id, e)

    def load_image_paths(self, ad_id):
        base_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "data")
        )
        directory_path = os.path.join(base_path, ad_id)
        image_folder_path = os.path.join(directory_path, "images")

        self.images_path = []

        if not os.path.exists(image_folder_path):
            self.logger.warning(f"No image folder found at: {image_folder_path}")
            return

        for file_name in os.listdir(image_folder_path):
            if file_name.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                full_path = os.path.join(image_folder_path, file_name)
                self.images_path.append(full_path)

        self.logger.info(
            f"Loaded {len(self.images_path)} image paths for ad_id: {ad_id}"
        )




if __name__ == "__main__":
    obj = MyHomeUploader("https://statements.myhome.ge/ka/statement/create?referrer=myhome", False)
    obj.load_data_json("19855161")
    obj.load_image_paths("19855161")
    obj.primary_authenticate()
    obj.open_page()
    obj.main_upload()
    """obj.additional_upload(
        livo=True,
        livo_vip=False,
        livo_vip_time=None,
        livo_facebook=False,
        livo_facebook_time=None,
        myhome_supervip=True,
        myhome_supervip_time="1 დღე",
        myhome_vipplus=True,
        myhome_vipplus_time="1 დღე",
        myhome_vip=True,
        myhome_vip_time="1 დღე",
        add_color=True,
        add_color_time="1 დღე",
        automate=True,
        automate_time_day="1 დღე",
        automate_time_hour="00:00 საათი"
    )"""
    obj.finish_upload()
    obj.close_browser()
    obj.save_to_excel()
