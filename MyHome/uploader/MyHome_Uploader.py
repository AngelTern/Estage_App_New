from BasicSeleniumSetup.BasicSetup import BasicScraper

"""--------------------------------------------------"""
import os
import json


class MyHomeUploader(BasicScraper):
    def __init__(self, headless=True, log_file="scraper.log"):
        self.data = None
        upload_url = "https://statements.myhome.ge/ka/statement/create?referrer=myhome"
        super().__init__(upload_url, headless, log_file)

    def load_json(self, ad_id):
        self.ad_id = ad_id
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
        print(base_path)
        directory_path = os.path.join(base_path, self.ad_id)
        print(directory_path)
        json_file_path = os.path.join(directory_path, f"{self.ad_id}.json")
        print(json_file_path)
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

    def main_upload(self):
        pass


if __name__ == "__main__":
    obj = MyHomeUploader()
    obj.load_json("19855161")
    obj.open_page()
    obj.main_upload()
    obj.close_browser()
    obj.save_to_excel()
