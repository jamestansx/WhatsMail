import os

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
        self.make_dir()
        return self.dirs

    def make_dir(self):
        for dir in self.dirs:
            try:
                os.makedirs(self.dirs[dir], exist_ok=True)
            except OSError:
                raise OSError
        return True


class CreateKey:
    userGmailAcc = ""

    def __init__(self):
        self.userPassword = ""

    def keyGen(self):
        CreateKey.userGmailAcc = input("Enter your G-mail account: ")
        self.userPassword = input("Enter your G-mail password: ")
        try:
            yagmail.register(CreateKey.userGmailAcc, self.userPassword)
            return True
        except Exception as e:
            error = f"Failed to register: {e}"
            raise error

    def delKey():
        try:
            keyring.delete_password("yagmail", CreateKey.userGmailAcc)
            return True
        except Exception as e:
            error = f"Failed to delete key: {e}"
            raise error

    def change_password():
        new_password = input("Enter new password: ")
        try:
            keyring.set_password("yagmail", CreateKey.userGmailAcc, new_password)
            return True
        except KeyError as e:
            error = f"Failed to change password: {e}"
            raise error


def getDirs(appname, appauthor):
    get_dirs = GetDirs(appname, appauthor)
    get_dirs.get_dirs()
