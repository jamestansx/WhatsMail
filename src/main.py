import os

import config
import fetchMessages
import log
import openmessages
import sendEmail
import setting
import websetup

target_username, gmail, download_path, webdriverPath, userGmail, chromedataPath, isFirstRun = (
    "",
    "",
    "",
    "",
    "",
    "",
    "",
)


def presetup():
    global target_username, gmail, download_path, webdriverPath, userGmail, chromedataPath
    log.loggerConfig()
    download_path, webdriverPath, chromedataPath, isFirstRun = config.isFirstRun()
    target_username, gmail, userGmail = config.isConfig()
    return websetup.open_whatsapp(download_path, webdriverPath, chromedataPath, isFirstRun)


def main():
    if openmessages.open_conversation(target_username) is True:
        message_list = fetchMessages.fetchMessages(download_path)
        sendEmail.sendGmail(userGmail, target_username, gmail, message_list, download_path)
    setting.remove_files(download_path)
    os.remove(log.userLog_path)


if __name__ == "__main__":
    if presetup() is True:
        main()
