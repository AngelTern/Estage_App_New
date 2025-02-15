import json
import os
import sys
import openpyxl
from PyQt5.QtCore import QThread, pyqtSignal
from MyHome.scraper.MyHome_Scraper import MyHomeScraper
from MyHome.uploader.MyHome_Uploader import MyHomeUploader
from SS.scraper.SS_Scraper import SS_Scraper
from SS.uploader.SS_Uploader import SS_Uploader


def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


class UploadWorker(QThread):
    finished = pyqtSignal()
    errorOccurred = pyqtSignal(str)

    def __init__(self, url, currency, agency_price, comment, upload_description, run_myhome, run_ss):
        super().__init__()
        self.url = url
        self.currency = currency
        self.agency_price = agency_price
        self.comment = comment
        self.upload_description = upload_description
        self.run_myhome = run_myhome
        self.run_ss = run_ss
        self.excel_path = os.path.join(get_base_dir(), "data", "realestate.xlsx")

    def run(self):
        try:
            url_lower = self.url.lower()
            if "myhome" in url_lower:
                lead = "myhome"
            elif "ss.ge" in url_lower:
                lead = "ss"
            else:
                raise ValueError("URL does not contain a valid lead identifier (myhome or ss.ge)")

            if lead == "myhome":
                scraper = MyHomeScraper(url=self.url)
                scraper.open_page()
                scraper.scrape_for_ad_id()
                scraper.main_scrape(currency_to_set=self.currency, agency_price=self.agency_price, comment=self.comment)
                scraper.get_images()
                scraper.close_browser()
                ad_id = scraper.save_to_json()
            elif lead == "ss":
                scraper = SS_Scraper(url=self.url, agency_price=self.agency_price, currency=self.currency,
                                     comment=self.comment, headless=False)
                ad_id = scraper.run()
                scraper.close_browser()

            if self.run_myhome:
                uploader_myhome = MyHomeUploader(url="https://statements.myhome.ge/ka/statement/create?referrer=myhome",
                                                 headless=False)
                uploader_myhome.load_data_json(ad_id)
                uploader_myhome.load_image_paths(ad_id)
                uploader_myhome.primary_authenticate()
                uploader_myhome.open_page()
                uploader_myhome.main_upload(self.upload_description)
                final_url_myhome = uploader_myhome.finish_upload()
                uploader_myhome.close_browser()
                uploader_myhome.save_to_excel()

            if self.run_ss:
                uploader_ss = SS_Uploader(url="https://home.ss.ge/ka/udzravi-qoneba/create", headless=False)
                final_url_ss = uploader_ss.run_upload(ad_id=ad_id if ad_id else "20445069", enter_description=True,
                                                   stop_event=None)

        except Exception as e:
            self.errorOccurred.emit(str(e))
        finally:
            # === New: Load corresponding JSON file at the beginning ===
            try:
                from datetime import datetime
                ad_id_val = ad_id if 'ad_id' in locals() else ""
                json_path = os.path.join(get_base_dir(), "data", ad_id_val, f"{ad_id_val}.json")
                if os.path.exists(json_path):
                    with open(json_path, "r", encoding="utf-8") as json_file:
                        json_data = json.load(json_file)
                        print("Loaded JSON data:", json_data)
                else:
                    print("JSON file not found at:", json_path)
            except Exception as json_error:
                self.errorOccurred.emit("JSON load error: " + str(json_error))
            # === End New: JSON load ===

            # === New: Append row of data to the Excel file ===
            try:
                wb = openpyxl.load_workbook(self.excel_path)
                ws = wb.active
                # Build row data using the desired columns:
                # ["Uploaded Timestamp", "მესაკუთრის ID", "ტელეფონის ნომერი",
                #  "რაიონი", "ოთახი", "სართული", "მისამართი", "სააგენტოს ფასი",
                #  "მესაკუთრის ფასი", "Comment", "ss.ge/myhome.ge"]
                row_data = [
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    ad_id_val,
                    json_data.get("phone_number"),  # Phone number
                    json_data.get("breadcrumbs").get("რაიონი"),  # რეგიონი
                    json_data.get("property_details").get("ოთახი"),  # ოთახი
                    json_data.get("property_details").get("სართული"),  # სართული
                    json_data.get("location") + json_data.get("number"),  # მისამართი
                    self.agency_price,
                    json_data.get("owner_price"),  # მესაკუთრის ფასი
                    self.comment,
                    final_url_ss if final_url_ss else "",
                    final_url_myhome if final_url_myhome else "",
                ]
                ws.append(row_data)
                wb.save(self.excel_path)
            except Exception as excel_error:
                self.errorOccurred.emit("Excel error: " + str(excel_error))
            # === End New: Excel update ===

            self.finished.emit()
