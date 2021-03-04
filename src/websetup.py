import sys

from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

shortdelay = 5
longdelay = 10
max_attempts = 3
ignore_exceptions = (StaleElementReferenceException, NoSuchElementException)
driver = None


class WebWhatsApp:
    def __init__(self, driverPath, downloadPath):
        self.URL = "https://web.whatsapp.com/"  # WhatsApp URL
        self.driverPath = driverPath
        self.chrome_option = Options()  # saving and loading the profile configuration
        self.prefs = {
            "download.default_directory": f"{downloadPath}",
            "safebrowsing.enabled": "false",
        }

    def setupSelenium(self):
        path = self.driverPath
        self.chrome_option.add_argument("--disable-notifications")
        self.chrome_option.add_argument(f"user-data-dir=D:/websession/")
        #self.chrome_option.add_experimental_option("prefs", self.prefs)
        # self.chrome_option.add_argument("--headless")
        # Uncomment this after the program is done
        # ============================================
        # load the webdriver and website configuration
        global driver
        driver = webdriver.Chrome(executable_path=path, options=self.chrome_option)
        driver.implicitly_wait(15)


    def is_loaded():
        attempts = 0
        while attempts <= max_attempts:
            try:  # wait for the webpage to load
                WebDriverWait(driver, longdelay).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "G8bNp"))
                )  # this will wait until the page is loaded
                print("Page is ready!")
                return True
            except TimeoutException:
                print("Loading took too much time!")
                print("Retrying...")
            attempts += 1
        if attempts > max_attempts:
            print("Too many attempts")
            input("Press Any Key to continue")
            driver.close()
            sys.exit(0)

    def open_webdriver(self):
        self.setupSelenium()
        driver.get(self.URL)
        return WebWhatsApp.is_loaded()

def open_whatsapp(downloadPath, webdriverPath):
    webwhatsapp = WebWhatsApp(webdriverPath, downloadPath)
    return webwhatsapp.open_webdriver()

def close_webdriver():
    driver.close()
