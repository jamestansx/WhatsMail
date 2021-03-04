import config
import websetup
import openmessages
import fetchMessages
import sendEmail

target_username, gmail, download_path, webdriverPath, userGmail, chromedataPath = "", "", "", "", "",""


def presetup():
    global target_username, gmail, download_path, webdriverPath, userGmail, chromedataPath

    download_path, webdriverPath, chromedataPath = config.isFirstRun()

    target_username, gmail, userGmail = config.isConfig()

    return websetup.open_whatsapp(download_path, webdriverPath, chromedataPath)


def main():
    if openmessages.open_conversation(target_username) is True:
        message_list = fetchMessages.fetchMessages()
        sendEmail.sendGmail(userGmail, target_username, gmail, message_list, download_path)


if __name__ == "__main__":
    if presetup() is True:
        main()
