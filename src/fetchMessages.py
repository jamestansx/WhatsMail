from selenium.webdriver.support.ui import WebDriverWait

import websetup


def fetchMessages():
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
                    download(message)
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


def download(message):
    try:
        download_pdf(message)
    except Exception:
        try:
            download_Img(message)
        except Exception as e:
            print(e)


def download_Img(message):
    image_container = message.find_element_by_xpath('.//div[contains(@role,"button")]')
    image_container.click()
    img_download_button_container = websetup.driver.find_elements_by_xpath(
        "//div[contains(@class,'_2n-zq')]"
    )
    for img in img_download_button_container:
        try:
            img_download_button = img.find_element_by_xpath(
                './/span[contains(@data-icon, "download")]'
            )
            img_download_button.click()
        except Exception:
            pass
        finally:
            exit_img(img_download_button)


def exit_img(img_download_button):
    try:
        exit_container = websetup.driver.find_element_by_xpath(
            "//div[contains(@class, '_1ljzS _2Ryya')]"
        )
        exit = exit_container.find_element_by_xpath(".//div[contains(@title, 'Close')]")
        exit.click()
        WebDriverWait(websetup.driver, websetup.longdelay).until_not(lambda x: img_download_button)
    except Exception:
        pass


def download_pdf(message):
    pdf = message.find_element_by_xpath('.//div[contains(@class,"MYzfD")]')
    pdf.click()
