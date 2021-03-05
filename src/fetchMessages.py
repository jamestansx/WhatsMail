from selenium.webdriver.support.ui import WebDriverWait
import time
import websetup
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

FileIsFounded = False


def fetchMessages(downloadPath):
    messages_class = websetup.driver.find_element_by_xpath("//div[@class='_11liR']")
    messages_elem_list = messages_class.find_elements_by_xpath(
        ".//div[contains(@class,'focusable-list-item')]"
    )
    isElemUnread = False
    messageList = []

    for message in messages_elem_list:
        if "UNREAD MESSAGE" in message.text:
            isElemUnread = True
            continue
        if isElemUnread is True:
            try:
                message = getMessage(message)
                messageList.append(message)
            except Exception:
                try:
                    download(message, downloadPath)
                except Exception as e:
                    print(e)
                    pass
    websetup.close_webdriver()
    return messageList


def getMessage(element):
    message_container = element.find_element_by_xpath(".//div[contains(@class, 'copyable-text')]")
    message = message_container.find_element_by_xpath(
        ".//span[contains(@class, '_3-8er selectable-text copyable-text')]"
    ).text
    return message


def download(message, downloadPath):
    try:
        download_pdf(message, downloadPath)
    except Exception:
        try:
            download_Img(message, downloadPath)
        except Exception as e:
            print(e)


def download_Img(message, downloadPath):
    image_container = message.find_element_by_xpath('.//div[contains(@role,"button")]')
    image_container.click()
    try:
        img_download_button = websetup.driver.find_element_by_xpath(
            '//*[@id="app"]/div/span[3]/div/div/div[2]/div[1]/div[2]/div/div[4]/div/span'
        )
        img_download_button.click()
    except Exception:
        pass
    finally:
        exit_img(downloadPath, img_download_button)


def exit_img(downloadPath, img_download_button):
    try:
        exit = websetup.driver.find_element_by_xpath(
            "//*[@id='app']/div/span[3]/div/div/div[2]/div[1]/div[2]/div/div[5]/div/span"
        )
        exit.click()
        WebDriverWait(websetup.driver, websetup.longdelay).until_not(lambda x: img_download_button)
        watch = OnMyWatch(downloadPath)
        watch.run()
    except Exception:
        pass


def download_pdf(message, downloadPath):
    pdf = message.find_element_by_xpath('.//div[contains(@class,"MYzfD")]')
    pdf.click()
    watch = OnMyWatch(downloadPath)
    watch.run()


class OnMyWatch:
    # Set the directory on watch
    def __init__(self, downloadPath):
        self.observer = Observer()
        self.watchDirectory = downloadPath

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive=True)
        self.observer.start()
        while FileIsFounded is not True:
            time.sleep(2)
        self.observer.stop()
        print("Observer Stopped")
        self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == "created":
            # Event is created, you can process it now
            global FileIsFounded
            print(f"{event.src_path}")
            FileIsFounded = True
