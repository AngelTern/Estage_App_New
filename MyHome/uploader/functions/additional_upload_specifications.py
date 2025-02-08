import time
from selenium.webdriver.common.by import By
from BasicSeleniumSetup.functions.is_loaded import is_loaded
from BasicSeleniumSetup.functions.click_element import click_element
from BasicSeleniumSetup.functions.send_keys_to_element import send_keys_to_element
from BasicSeleniumSetup.functions.scroll_to_element import scroll_to_element_centered
import re

def additional_upload_specifications(scraper, by,
                                     value_myhome_supervip, value_myhome_supervip_input, value_myhome_supervip_select,
                                     myhome_supervip, myhome_supervip_time,
                                     value_myhome_vipplus, value_myhome_vipplus_input, value_myhome_vipplus_select,
                                     myhome_vipplus, myhome_vipplus_time,
                                     value_myhome_vip, value_myhome_vip_input, value_myhome_vip_select, myhome_vip,
                                     myhome_vip_time,
                                     value_add_color, value_add_color_input, value_add_color_select, add_color,
                                     add_color_time,
                                     value_automate, value_automate_time_day_input, value_automate_time_day_select,
                                     value_automate_time_hour_input, value_automate_time_hour_select,
                                     automate, automate_time_day, automate_time_hour,
                                     value_livo, livo,
                                     value_livo_vip, value_livo_vip_time_input, value_livo_vip_time_select,
                                     livo_vip, livo_vip_time,
                                     value_livo_facebook, value_livo_facebook_input, value_livo_facebook_select,
                                     livo_facebook, livo_facebook_time):
    def select_option(button_value, input_value, select_value, option_text, option_name):
        try:
            if not option_text:
                return
            button = scraper.driver.find_element(by, button_value)
            if not click_element(scraper, by, button):
                scraper.logger.error(f"Failed to click on {option_name} button.")
                return False
            input_element = scraper.driver.find_element(by, input_value)
            if not click_element(scraper, by, input_element):
                scraper.logger.error(f"Failed to click on {option_name} input field.")
                return False
            time.sleep(0.4)
            select_elements = scraper.driver.find_elements(by, select_value)
            for element in select_elements:
                if element.text.strip() == option_text:
                    if not click_element(scraper, by, element):
                        scraper.logger.error(f"Failed to select {option_name}.")
                        return False
                    break
            return True
        except Exception as e:
            scraper.logger.error(f"Exception occurred in {option_name} selection: {str(e)}")
            return False

    livo_button_element = scraper.driver.find_element(by, value_livo)
    livo_data_state = livo_button_element.get_attribute("data-state")

    if livo_data_state != "checked":
        try:
            click_element(scraper, by, livo_button_element)
            time.sleep(0.5)
        except Exception as e:
            scraper.logger.error(f"Failed to click Livo button: {str(e)}")

    if myhome_supervip:
        select_option(value_myhome_supervip, value_myhome_supervip_input, value_myhome_supervip_select,
                      myhome_supervip_time, "myhome_supervip")
    else:
        myhome_supervip_button_element = scraper.driver.find_element(by, value_myhome_supervip)
        try:
            scraper.driver.execute_script("arguments[0].click();", myhome_supervip_button_element)
        except Exception as e:
            scraper.logger.error(f"Failed to unclick myhome_supervip button via JS: {str(e)}")
            return

    if myhome_vipplus:
        select_option(value_myhome_vipplus, value_myhome_vipplus_input, value_myhome_vipplus_select,
                      myhome_vipplus_time, "myhome_vipplus")

    if myhome_vip:
        select_option(value_myhome_vip, value_myhome_vip_input, value_myhome_vip_select, myhome_vip_time,
                      "myhome_vip")

    if add_color:
        select_option(value_add_color, value_add_color_input, value_add_color_select, add_color_time, "add_color")

    if automate:
        try:
            automate_button = scraper.driver.find_element(by, value_automate)
            if not click_element(scraper, by, automate_button):
                scraper.logger.error("Failed to click on automate button.")
                return
            if automate_time_day:
                automate_time_day_input_element = scraper.driver.find_element(by, value_automate_time_day_input)
                if not click_element(scraper, by, automate_time_day_input_element):
                    scraper.logger.error("Failed to click on automate_time_day input.")
                    return
                time.sleep(0.4)
                automate_time_day_select_elements = scraper.driver.find_elements(by, value_automate_time_day_select)
                for element in automate_time_day_select_elements:
                    if element.text.strip() == automate_time_day:
                        if not click_element(scraper, by, element):
                            scraper.logger.error("Failed to select automate_time_day.")
                            return
                        break
            if automate_time_hour:
                automate_time_hour_input_element = scraper.driver.find_element(by, value_automate_time_hour_input)
                if not click_element(scraper, by, automate_time_hour_input_element):
                    scraper.logger.error("Failed to click on automate_time_hour input.")
                    return
                time.sleep(0.4)
                automate_time_hour_select_elements = scraper.driver.find_elements(by, value_automate_time_hour_select)
                for element in automate_time_hour_select_elements:
                    if element.text.strip() == automate_time_hour:
                        if not click_element(scraper, by, element):
                            scraper.logger.error("Failed to select automate_time_hour.")
                            return
                        break
        except Exception as e:
            scraper.logger.error(f"Exception occurred in automate selection: {str(e)}")

    if not scroll_to_element_centered(scraper, by, value_livo):
        scraper.logger.warning("Could not scroll down to Livo button.")
        return

    livo_button_element = scraper.driver.find_element(by, value_livo)
    livo_data_state = livo_button_element.get_attribute("data-state")

    if livo is True and livo_data_state != "checked":
        try:
            click_element(scraper, by, livo_button_element)
        except Exception as e:
            scraper.logger.error(f"Failed to click Livo button: {str(e)}")

    if livo is False and livo_data_state == "checked":
        try:
            click_element(scraper, by, livo_button_element)
        except Exception as e:
            scraper.logger.error(f"Failed to unclick Livo button: {str(e)}")

    if livo_vip:
        select_option(value_livo_vip, value_livo_vip_time_input, value_livo_vip_time_select, livo_vip_time, "livo_vip")

    if livo_facebook:
        select_option(value_livo_facebook, value_livo_facebook_input, value_livo_facebook_select,
                      livo_facebook_time, "livo_facebook")
