import sys

from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import websetup

username_elem = None


def open_conversation(target_username):
    global username_elem
    username_elem = websetup.driver.find_element_by_xpath(
        f"//span[@title='{target_username}']"
    )  # find the target's chatbar
    if check_status() is True:
        click_box()
    is_chat_loaded()


def check_status():
    while True:
        try:
            username_class = username_elem.find_element_by_xpath(".//ancestor::div[@class='TbtXF']")
            unread_status = username_class.find_element_by_xpath(".//span[@class='_38M1B']")
            print(f"unread_status: {unread_status.text}")
            return True
        except (NoSuchElementException, TimeoutException) as e:
            print("**No new messages**")
            print(f"Details: {e}")
            input("Press Any Key to continue")
            websetup.driver.close()
            sys.exit(0)
        except StaleElementReferenceException:
            pass


def click_box():
    while True:
        try:
            username_elem.click()
            break
        except Exception as e:
            print(f"*******\n{e}")
            continue


def is_chat_loaded():
    attempts = 0
    while attempts < websetup.max_attempts:
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
            print("chat opened")
            input("Enter to continue...")
            return True
        except Exception:
            attempts += 1
            pass
    return False
