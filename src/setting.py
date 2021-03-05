import os
import logging

import keyring
import yagmail
from appdirs import AppDirs


class GetDirs:
    def __init__(self, appname, appauthor):
        self.appname = appname
        self.appauthor = appauthor
        self.dirs = {}

    def get_dirs(self):
        dir = AppDirs(self.appname, self.appauthor)
        self.dirs["userData"] = dir.user_data_dir
        self.dirs["userCache"] = dir.user_cache_dir
        self.dirs["userLog"] = dir.user_log_dir
        self.dirs["userConfig"] = dir.user_config_dir
        self.make_dir()
        return self.dirs

    def make_dir(self):
        for dir in self.dirs:
            try:
                os.makedirs(self.dirs[dir], exist_ok=True)
            except OSError:
                logging.error("Could not create directory")
        return True


class target:
    def __init__(self):
        self.username = None
        self.gmail = None

    def newTarget(self):
        self.username = input("Enter new WhatsApp contact: ")
        self.gmail = input("Enter new recipient's Gmail contact: ")
        return self.username, self.gmail


class Key:
    userGmailAcc = ""

    def __init__(self):
        self.userPassword = ""

    def keyGen(self):
        Key.userGmailAcc = input("Enter your G-mail account: ")
        self.userPassword = input("Enter your G-mail password: ")
        try:
            yagmail.register(Key.userGmailAcc, self.userPassword)
            logging.info(f"Successfully register {Key.userGmailAcc} key")
            return True
        except Exception as e:
            error = f"Failed to register: {e}"
            logging.error(error)

    def delKey():
        try:
            keyring.delete_password("yagmail", Key.userGmailAcc)
            return True
        except Exception as e:
            error = f"Failed to delete key: {e}"
            logging.error(error)

    def change_password():
        new_password = input("Enter new password: ")
        try:
            keyring.set_password("yagmail", Key.userGmailAcc, new_password)
            return True
        except KeyError as e:
            error = f"Failed to change password: {e}"
            logging.error(error)


def getDirs(appname, appauthor):
    get_dirs = GetDirs(appname, appauthor)
    logging.debug("directory(s) is created")
    return get_dirs.get_dirs()

def getLogDir(appname, appauthor):
    dir = AppDirs(appname, appauthor)
    logdir = dir.user_log_dir
    return logdir

def remove_files(dirPath):
    for file in os.listdir(dirPath):
        os.remove(os.path.join(dirPath, file))
    logging.info(f"all files in {dirPath} is deleted")
