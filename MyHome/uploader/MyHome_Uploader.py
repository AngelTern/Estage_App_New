from BasicSeleniumSetup.BasicSetup import BasicScraper
from MyHome.uploader.MyHome_Upload_Selectors import MyHomeUploadSelectors
from MyHome.uploader.functions.authentication_process import authenticate
from MyHome.uploader.functions.choose_property_type import choose_property_type
from MyHome.uploader.functions.choose_transaction_type import choose_transaction_type
from MyHome.uploader.functions.choose_city import choose_city

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


        time.sleep(10000)




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


if __name__ == "__main__":
    obj = MyHomeUploader("https://statements.myhome.ge/ka/statement/create?referrer=myhome", False)
    obj.load_data_json("19855161")
    obj.primary_authenticate()
    obj.open_page()
    obj.main_upload()
    obj.close_browser()
    obj.save_to_excel()
