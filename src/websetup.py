import sys
import os
import logging

from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import jsonfile
import setting
import config

shortdelay = 5
longdelay = 10
max_attempts = 3
ignore_exceptions = (StaleElementReferenceException, NoSuchElementException)
driver = None


class WebWhatsApp:
    def __init__(self, driverPath, downloadPath, chromedataPath):
        self.URL = "https://web.whatsapp.com/"  # WhatsApp URL
        self.driverPath = driverPath
        self.chrome_option = Options()  # saving and loading the profile configuration
        self.chromedataPath = chromedataPath
        self.prefs = {
            "download.default_directory": f"{downloadPath}\\",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False,
        }
        logging.debug("__init__ is initiated")

    def setupSelenium(self, isFirstRun):
        global driver
        path = self.driverPath
        if isFirstRun is False:
            self.chrome_option.add_argument("--headless")
            dirs = setting.getDirs(config.appname, config.appauthor)
            userData_json = os.path.join(dirs["userData"], "data.json")
            data = jsonfile.read_json(userData_json)
            user_agent = data["user_agent"]
            self.chrome_option.add_argument("--user-agent={}".format(user_agent))
            logging.debug(f"Options* are loaded --isFirstRun: {isFirstRun}--")
        self.chrome_option.add_argument("--no-sandbox")
        self.chrome_option.add_argument("--disable-notifications")
        self.chrome_option.add_argument("--disable-gpu")
        self.chrome_option.add_argument(f"user-data-dir={self.chromedataPath}")
        self.chrome_option.add_experimental_option("prefs", self.prefs)
        driver = webdriver.Chrome(executable_path=path, options=self.chrome_option)
        logging.debug("Essential options are loaded")
        if isFirstRun is True:
            user_agent = driver.execute_script("return navigator.userAgent;")
            dirs = setting.getDirs(config.appname, config.appauthor)
            userData_json = os.path.join(dirs["userData"], "data.json")
            data = jsonfile.read_json(userData_json)
            data["user_agent"] = user_agent
            data["isFirstRun"] = False
            jsonfile.updata_json(userData_json, data)
            logging.debug("First time options is ran")
        driver.implicitly_wait(10)

    def is_loaded():
        attempts = 0
        while attempts <= max_attempts:
            try:  # wait for the webpage to load
                WebDriverWait(driver, longdelay).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "G8bNp"))
                )  # this will wait until the page is loaded
                logging.info("Page is loaded")
                return True
            except TimeoutException:
                logging.debug("Took too long to load(!)")
            attempts += 1
        if attempts > max_attempts:
            logging.error("Too many attempts trying to load the page!!")
            driver.close()
            sys.exit(0)

    def open_webdriver(self, isFirstRun):
        self.setupSelenium(isFirstRun)
        driver.get(self.URL)
        if isFirstRun is True:
            print("Scan QR Code, And then Enter")
            input()
            print("Logged In")
            logging.info("QR code is scanned")
        return WebWhatsApp.is_loaded()


def open_whatsapp(downloadPath, webdriverPath, chromedataPath, isFirstRun):
    webwhatsapp = WebWhatsApp(webdriverPath, downloadPath, chromedataPath)
    return webwhatsapp.open_webdriver(isFirstRun)


def close_webdriver():
    driver.close()
    logging.info("Driver is closed")
