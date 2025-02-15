import os
import sys
import time
import json
import pyperclip
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from BasicSeleniumSetup.BasicSetup import BasicScraper


def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))


logging.basicConfig(filename=os.path.join(get_base_dir(), 'uploader.log'),
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


class SS_Uploader(BasicScraper):
    def __init__(self, url, headless=False, log_file="scraper.log"):
        super().__init__(url, headless=headless)
        self.driver = None

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
            if stop_event and stop_event.wait(poll_frequency):
                return False
            if time.time() > end_time:
                break
        return False

    @staticmethod
    def click_element(driver, locator, stop_event=None):
        def condition():
            element = driver.find_element(*locator)
            if element.is_displayed() and element.is_enabled():
                element.click()
                return True
            return False

        return SS_Uploader.custom_wait(driver, condition_function=condition, timeout=10, poll_frequency=0.1,
                                       stop_event=stop_event)

    @staticmethod
    def send_keys_to_element(driver, locator, keys, stop_event=None):
        def condition():
            element = driver.find_element(*locator)
            element.clear()
            element.send_keys(keys)
            return True

        return SS_Uploader.custom_wait(driver, condition_function=condition, timeout=10, poll_frequency=0.5,
                                       stop_event=stop_event)

    @staticmethod
    def indefinite_click_next(driver, locator, stop_event=None):
        while True:
            if stop_event and stop_event.is_set():
                return False
            try:
                SS_Uploader.click_element(driver, locator, stop_event)
                time.sleep(1.0)
                return True
            except (NoSuchElementException, ElementClickInterceptedException):
                time.sleep(0.5)
            except Exception as e:
                time.sleep(0.5)

    @staticmethod
    def wait_for_final_element_indefinitely(driver, locator, stop_event=None):
        while True:
            if stop_event and stop_event.is_set():
                return None
            time.sleep(0.5)
            try:
                final_button = driver.find_element(*locator)
                final_button.click()
                time.sleep(0.1)
                final_url = pyperclip.paste()
                if final_url:
                    return final_url
            except NoSuchElementException:
                pass
            except Exception as e:
                pass

    def run_upload(self, username, password, phone_number, ad_id, enter_description=True, stop_event=None,
                   output_dir=None):
        if output_dir is None:
            logging.error("Output directory not provided to run_upload.")
            return None
        #print(output_dir)
        data_folder = os.path.join(output_dir, ad_id)
        json_file_path = os.path.join(data_folder, f"{ad_id}.json")
        logging.info(f"Uploader looking for JSON file at: {json_file_path}")
        if not os.path.exists(json_file_path):
            logging.error(f"JSON file not found at: {json_file_path}")
            return None
        try:
            with open(json_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            logging.error(f"Error reading JSON file: {e}")
            return None
        options = Options()
        if self.headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        final_url = None
        try:
            if stop_event and stop_event.is_set():
                self.driver.quit()
                return None
            self.driver.get("https://home.ss.ge/ka/udzravi-qoneba/create")
            if stop_event and stop_event.is_set():
                self.driver.quit()
                return None
            login_locator = (By.CLASS_NAME, "sc-8ce7b879-10")
            if not SS_Uploader.click_element(self.driver, login_locator, stop_event=stop_event):
                self.driver.quit()
                return None
            if not SS_Uploader.send_keys_to_element(self.driver, (By.NAME, "email"), username, stop_event=stop_event):
                self.driver.quit()
                return None
            if not SS_Uploader.send_keys_to_element(self.driver, (By.NAME, "password"), password,
                                                    stop_event=stop_event):
                self.driver.quit()
                return None
            submit_locator = (By.CSS_SELECTOR, "button.sc-1c794266-1.cFcCnt")
            if not SS_Uploader.click_element(self.driver, submit_locator, stop_event=stop_event):
                self.driver.quit()
                return None
            add_new_button_path = (By.CSS_SELECTOR, "div.sc-b3bd94d2-0.kmSDJX > button.sc-1c794266-1.eqszNP")
            add_new_button_element = self.driver.find_elements(*add_new_button_path)
            if add_new_button_element:
                if not SS_Uploader.click_element(self.driver, add_new_button_path, stop_event=stop_event):
                    self.driver.quit()
                    return None
            if stop_event and stop_event.is_set():
                self.driver.quit()
                return None
            property_type = data.get("breadcrumbs", {}).get("property_type")
            if property_type:
                property_locator = (By.XPATH, f"//div[text()='{property_type}']")
                if not SS_Uploader.click_element(self.driver, property_locator, stop_event=stop_event):
                    self.driver.quit()
                    return None
            if stop_event and stop_event.is_set():
                self.driver.quit()
                return None
            time.sleep(0.2)
            transaction_type = data.get("breadcrumbs", {}).get("transaction_type")
            if transaction_type:
                transaction_locator = (By.XPATH, f"//div[text()='{transaction_type}']")
                if not SS_Uploader.click_element(self.driver, transaction_locator, stop_event=stop_event):
                    self.driver.quit()
                    return None
            if stop_event and stop_event.is_set():
                self.driver.quit()
                return None
            time.sleep(0.2)
            image_folder = os.path.join(data_folder, "images")
            if os.path.exists(image_folder):
                image_paths = [os.path.abspath(os.path.join(image_folder, img))
                               for img in os.listdir(image_folder)
                               if img.lower().endswith((".png", ".jpg", ".jpeg"))]
                if image_paths:
                    for image_path in image_paths:
                        if stop_event and stop_event.is_set():
                            self.driver.quit()
                            return None
                        try:
                            image_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
                            image_input.send_keys(image_path)
                            if stop_event and stop_event.wait(0.5):
                                self.driver.quit()
                                return None
                        except Exception as e:
                            logging.warning(f"Could not upload image {image_path}: {e}")
            if stop_event and stop_event.is_set():
                self.driver.quit()
                return None
            time.sleep(0.2)
            location = data.get("location", "")
            if location:
                address_locator = (By.CSS_SELECTOR, "input#react-select-3-input.select__input")
                if not SS_Uploader.send_keys_to_element(self.driver, address_locator, location, stop_event=stop_event):
                    self.driver.quit()
                    return None
                if stop_event and stop_event.wait(0.5):
                    self.driver.quit()
                    return None
                try:
                    address_input = self.driver.find_element(*address_locator)
                    address_input.send_keys(Keys.DOWN)
                    address_input.send_keys(Keys.ENTER)
                except Exception as e:
                    logging.warning(f"Failed to select location from dropdown: {e}")
            time.sleep(0.2)
            if stop_event and stop_event.is_set():
                self.driver.quit()
                return None
            number = data.get("number")
            if number:
                number_input_locator = (By.CSS_SELECTOR,
                                        "#create-app-loc > div.sc-bb305ae5-3.iDHOHS > div.sc-bb305ae5-4.VxicA > div:nth-child(2) > label > div > input")
                if not SS_Uploader.send_keys_to_element(self.driver, number_input_locator, number,
                                                        stop_event=stop_event):
                    self.driver.quit()
                    return None
            time.sleep(0.2)
            rooms = data.get("property_details", {}).get("ოთახი", "")
            if rooms:
                rooms_locator = (By.XPATH, f"//div[@class='sc-226b651b-0 kgzsHg']/p[text()='{rooms}']")
                if not SS_Uploader.click_element(self.driver, rooms_locator, stop_event=stop_event):
                    self.driver.quit()
                    return None
            time.sleep(0.2)
            bedrooms = data.get("property_details", {}).get("საძინებელი", "")
            if bedrooms:
                bedrooms_locator = (By.XPATH,
                                    f"//div[@class='sc-e8a87f7a-0 dMKNFB']/div[@class='sc-e8a87f7a-1 bilVxg'][2]/div[@class='sc-e8a87f7a-3 gdEkZl']/div[@class='sc-e8a87f7a-4 jdtBxj']/div[@class='sc-226b651b-0 kgzsHg']/p[text()='{bedrooms}']")
                if not SS_Uploader.click_element(self.driver, bedrooms_locator, stop_event=stop_event):
                    self.driver.quit()
                    return None
            if stop_event and stop_event.is_set():
                self.driver.quit()
                return None
            time.sleep(0.2)
            total_area = data.get("property_details", {}).get("საერთო ფართი", "")
            if total_area:
                total_area_locator = (By.NAME, "totalArea")
                if not SS_Uploader.send_keys_to_element(self.driver, total_area_locator, total_area,
                                                        stop_event=stop_event):
                    self.driver.quit()
                    return None
            if stop_event and stop_event.is_set():
                self.driver.quit()
                return None
            time.sleep(0.2)
            floor = data.get("property_details", {}).get("სართული", "")
            if floor:
                floor_locator = (By.NAME, "floor")
                if not SS_Uploader.send_keys_to_element(self.driver, floor_locator, floor, stop_event=stop_event):
                    self.driver.quit()
                    return None
            if stop_event and stop_event.is_set():
                self.driver.quit()
                return None
            time.sleep(0.2)
            floors = data.get("property_details", {}).get("სართულიანობა", "")
            if floors:
                floors_locator = (By.NAME, "floors")
                if not SS_Uploader.send_keys_to_element(self.driver, floors_locator, floors, stop_event=stop_event):
                    self.driver.quit()
                    return None
            if stop_event and stop_event.is_set():
                self.driver.quit()
                return None
            time.sleep(0.2)
            bathroom_count = data.get("additional_info", {}).get("სველი წერტილი", "")
            if bathroom_count:
                try:
                    bathroom_section = self.driver.find_element(By.ID, "create-app-details")
                    container_div = bathroom_section.find_element(By.CLASS_NAME, "sc-e8a87f7a-0.dMKNFB")
                    specific_div = container_div.find_elements(By.CLASS_NAME, "sc-e8a87f7a-1.bilVxg")[6]
                    gdEkZl_div = specific_div.find_element(By.CLASS_NAME, "sc-e8a87f7a-3.gdEkZl")
                    jdtBxj_div = gdEkZl_div.find_element(By.CLASS_NAME, "sc-e8a87f7a-4.jdtBxj")
                    bathroom_divs = jdtBxj_div.find_elements(By.CLASS_NAME, "sc-226b651b-0.kgzsHg")
                    for div in bathroom_divs:
                        if stop_event and stop_event.is_set():
                            self.driver.quit()
                            return None
                        if div.find_element(By.TAG_NAME, "p").text == bathroom_count:
                            div.click()
                            break
                except Exception as e:
                    logging.warning(f"Failed to set bathroom count: {e}")
            if stop_event and stop_event.is_set():
                self.driver.quit()
                return None
            time.sleep(0.2)
            status = data.get("additional_info", {}).get("სტატუსი", "")
            if status:
                status_locator = (By.XPATH, f"//div[@class='sc-226b651b-0 kgzsHg']/p[text()='{status}']")
                if not SS_Uploader.click_element(self.driver, status_locator, stop_event=stop_event):
                    self.driver.quit()
                    return None
            if stop_event and stop_event.is_set():
                self.driver.quit()
                return None
            time.sleep(0.2)
            condition = data.get("additional_info", {}).get("მდგომარეობა", "")
            if condition:
                condition_locator = (By.XPATH, f"//div[@class='sc-226b651b-0 kgzsHg']/p[text()='{condition}']")
                if not SS_Uploader.click_element(self.driver, condition_locator, stop_event=stop_event):
                    self.driver.quit()
                    return None
            if stop_event and stop_event.is_set():
                self.driver.quit()
                return None
            time.sleep(0.2)
            features = data.get("features", {})
            if features:
                feature_divs = self.driver.find_elements(By.XPATH,
                                                         "//div[@class='sc-226b651b-0 sc-226b651b-1 kgzsHg LZoqF']")
                for feature_div in feature_divs:
                    if stop_event and stop_event.is_set():
                        self.driver.quit()
                        return None
                    feature_name = feature_div.find_element(By.TAG_NAME, "p").text
                    if features.get(feature_name, "") == "კი":
                        try:
                            feature_div.click()
                        except Exception as e:
                            logging.warning(f"Could not click feature {feature_name}: {e}")
            if stop_event and stop_event.is_set():
                self.driver.quit()
                return None
            time.sleep(0.2)
            if enter_description:
                description = data.get("description", "")
                if description:
                    description_locator = (By.CSS_SELECTOR, "div.sc-4ccf129b-2.blumtp textarea")
                    if not SS_Uploader.send_keys_to_element(self.driver, description_locator, description,
                                                            stop_event=stop_event):
                        self.driver.quit()
                        return None
            if stop_event and stop_event.is_set():
                self.driver.quit()
                return None
            time.sleep(0.2)
            agency_price = data.get("agency_price", "")
            if agency_price:
                try:
                    agency_price_div = self.driver.find_element(By.ID, "create-app-price")
                    container_div = agency_price_div.find_element(By.CLASS_NAME, "sc-9c9d017-2.jKKqhD")
                    labels = container_div.find_elements(By.TAG_NAME, "label")
                    for label in labels:
                        if stop_event and stop_event.is_set():
                            self.driver.quit()
                            return None
                        if "active" not in label.get_attribute("class"):
                            label.click()
                            agency_price_input = label.find_element(By.TAG_NAME, "input")
                            agency_price_input.clear()
                            agency_price_input.send_keys(agency_price)
                            break
                except Exception as e:
                    logging.warning(f"Could not set agency price: {e}")
            if stop_event and stop_event.is_set():
                self.driver.quit()
                return None
            time.sleep(0.2)
            whatsapp_label_selector = (By.CSS_SELECTOR, "label.whatsappLabel")
            if not SS_Uploader.click_element(self.driver, whatsapp_label_selector, stop_event):
                self.driver.quit()
                return None
            time.sleep(0.5)
            next_button = (By.CSS_SELECTOR, "div.sc-1be1d6a8-0.fFjpQW > button.sc-1c794266-1.dICGws.btn-next")
            publish_button = (By.CSS_SELECTOR, ".sc-1c794266-1.ieRIPq")
            publish_button_2 = (By.CSS_SELECTOR, ".sc-1c794266-1.cFcCnt")

            def click_next_and_wait(driver, next_button, publish_button, publish_button_2, stop_event=None):
                try:
                    if not SS_Uploader.click_element(driver, next_button, stop_event):
                        try:
                            next_button_element = driver.find_element(*next_button)
                            driver.execute_script("arguments[0].click();", next_button_element)
                        except Exception as e:
                            return False

                    def publish_condition():
                        try:
                            publish_1 = driver.find_element(*publish_button)
                            if publish_1.is_displayed() and publish_1.is_enabled():
                                return True
                        except Exception:
                            pass
                        try:
                            publish_2 = driver.find_element(*publish_button_2)
                            if publish_2.is_displayed() and publish_2.is_enabled():
                                return True
                        except Exception:
                            pass
                        return False

                    if not SS_Uploader.custom_wait(driver, condition_function=publish_condition, timeout=10,
                                                   poll_frequency=0.2, stop_event=stop_event):
                        return False
                    return True
                except Exception as e:
                    return False

            if not click_next_and_wait(self.driver, next_button, publish_button, publish_button_2, stop_event):
                self.driver.quit()
                return None
            if not SS_Uploader.click_element(self.driver, publish_button, stop_event):
                if not SS_Uploader.click_element(self.driver, publish_button_2, stop_event):
                    self.driver.quit()
                    return None
            final_element_locator = (
            By.CSS_SELECTOR, "#__next > div.sc-af3cf45-0.fWBmkz > div.sc-af3cf45-6.ijmwBP > button.hBiInR")
            final_url = SS_Uploader.wait_for_final_element_indefinitely(self.driver, final_element_locator,
                                                                        stop_event=stop_event)
            if final_url:
                self.logger.info(f"Final url: {final_url}")
                return final_url
            else:
                return None
        except Exception as e:
            logging.error(f"Error occurred in run_uploader: {e}", exc_info=True)
            return None
        finally:
            self.driver.quit()


if __name__ == "__main__":
    uploader = SS_Uploader(url="https://home.ss.ge/ka/udzravi-qoneba/create", headless=False)
    final_url = uploader.run_upload(username="georgepapava2@gmail.com", password="george11032003",
                                    phone_number="your_phone", ad_id="6541544", enter_description=True, stop_event=None,
                                    output_dir=os.path.join(get_base_dir(), "data"))