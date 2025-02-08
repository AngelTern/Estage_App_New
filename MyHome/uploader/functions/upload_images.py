from selenium.webdriver.common.by import By
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.click_element import click_element
from BasicSeleniumSetup.functions.send_keys_to_element import send_keys_to_element
from BasicSeleniumSetup.functions.scroll_to_element import scroll_to_element_centered
import time
import re


def upload_images(scraper, by, value, value_after_one, value_div, images_list):
    try:
        image_input = scraper.driver.find_element(by, value)
        scraper.driver.execute_script(
            "arguments[0].removeAttribute('hidden');"
            "arguments[0].style.display='block';",
            image_input
        )
        if not scroll_to_element_centered(scraper, by, value):
            scraper.logger.warning("Could not scroll down to images input.")
            return
        counter = 1
        for image_path in images_list:
            if counter == 1:
                if not is_loaded(scraper, by, value):
                    scraper.logger.error("Image upload input did not load for first image.")
                    return
                scraper.logger.info(f"Uploading image: {image_path}")
                send_keys_to_element(scraper, by, value, image_path)
                time.sleep(0.5)
            else:
                scraper.logger.info("Attempting to locate second input element for subsequent images.")
                try:
                    second_input = scraper.driver.find_element(by, value_after_one)
                    scraper.logger.info(f"Found second input element: {second_input}")
                    scraper.driver.execute_script(
                        "arguments[0].removeAttribute('hidden');"
                        "arguments[0].style.display='block';",
                        second_input
                    )
                except Exception as e:
                    scraper.logger.error(f"Could not locate second input element using selector {value_after_one}: {e}")
                    return
                if not is_loaded(scraper, by, value_after_one, timeout=20):
                    scraper.logger.error("Image upload input did not load for subsequent images.")
                    return
                scraper.logger.info(f"Uploading image: {image_path}")
                send_keys_to_element(scraper, by, value_after_one, image_path)
                time.sleep(0.2)
            if not is_loaded(scraper, by, value_div, timeout=10):
                scraper.logger.error(f"Expected div element did not appear after uploading image: {image_path}")
                return
            counter += 1
        scraper.logger.info("Successfully attempted to upload all images.")
        return True
    except Exception as e:
        scraper.logger.error(f"Exception occurred in image upload process: {str(e)}")
