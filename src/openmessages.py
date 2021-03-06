import logging
import sys
import time

from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import websetup

username_elem = None


def open_conversation(target_username):
    global username_elem
    time.sleep(3)
    time_start = time.time()
    while time.time() < time_start + 30:
        try:
            username_elem = websetup.driver.find_element_by_xpath(
                f"//span[@title='{target_username}']"
            )  # find the target's chatbar
            logging.info(f"Contact: {username_elem.text}is found")
            break
        except Exception as e:
            logging.warning(f"Contact: {target_username } is not found - {e}")
            continue
    if check_status(target_username) is True:
        return is_chat_loaded()


def check_status(target_username):
    while True:
        try:
            username_class = username_elem.find_element_by_xpath(".//ancestor::div[@class='TbtXF']")
            unread_status = username_class.find_element_by_xpath(".//span[@class='_38M1B']")
            logging.debug(f"unread_status: {unread_status.text}")
            click_box(target_username)
            return True
        except (NoSuchElementException, TimeoutException) as e:
            logging.warning(f"No new message \nDetails: {e}")
            websetup.driver.close()
            sys.exit(0)
        except Exception as e:
            logging.error(e)
            pass


def click_box(target_username):
    time.sleep(2)
    global username_elem
    while True:
        try:
            username_elem.click()
            logging.debug("Chatbox is clicked")
            break
        except Exception as E:
            logging.warning(f"Chatbox is not clicked. Details: {E}")
            username_elem = websetup.driver.find_element_by_xpath(
                f"//span[@title='{target_username}']"
            )


def is_chat_loaded():
    while True:
        try:
            websetup.driver.find_element_by_xpath(
                '//*[@id="main"]/div[3]/div/div/div[2]/div[contains(@title,"loading messages…")]'
            )
            WebDriverWait(websetup.driver, websetup.shortdelay).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="main"]/div[3]/div/div/div[2]/div[contains(@title,"loading messages…")]',
                    )
                )
            )
            # then wait for the element to disappearprint   ("loaded messages...")
            WebDriverWait(websetup.driver, websetup.longdelay).until_not(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="main"]/div[3]/div/div/div[2]/div[contains(@title,"loading messages…")]',
                    )
                )
            )
            logging.debug("message is loaded")
            return True
        except (TimeoutException, NoSuchElementException) as e:
            logging.warning(f"message is loaded but with {e}")
            return True
