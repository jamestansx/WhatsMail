import os

import setting
import jsonfile

appname = "WhatsMail"
appauthor = "jamestansx"
dirs = ""
userDict = {}


def isFirstRun():
    global dirs
    dirs = setting.getDirs(appname, appauthor)
    userData_json = os.path.join(dirs["userData"], "data.json")
    if os.path.isfile(userData_json):
        return getSettings(userData_json)
    else:
        return setupSetting(userData_json)


def isConfig():
    userConfig_json = os.path.join(dirs["userConfig"], "config.json")
    if os.path.isfile(userConfig_json):
        return getConfig(userConfig_json)
    else:
        return setupConfig(userConfig_json)


def setupSetting(pathToFile):
    download_path = input("Please enter the download path: ")
    webdriverPath = input("Please enter the path to the Chrome webdriver: ")
    jsonfile.write_json(pathToFile, writeSettings(download_path, webdriverPath))
    global userDict
    userDict = createKey(pathToFile)
    return download_path, webdriverPath


def setupConfig(pathToFile):
    target = setting.target()
    username, gmail = target.newTarget()
    targetDict = {"username": username, "gmail": gmail}
    jsonfile.write_json(pathToFile, writeConfig(targetDict, userDict))
    return username, gmail, userDict["userGmail"]


def getSettings(pathToFile):
    data = jsonfile.read_json(pathToFile)
    try:
        if data["isFirstRun"] is not False:
            return setupSetting(pathToFile)
        if data["keyStatus"] is False:
            global userDict
            userDict = createKey(pathToFile)
    except Exception as e:
        raise e
    path = data["path"]
    downloadPath, webdriverPath = None, None
    for key in path:
        if os.path.isfile(path[key]) is True:
            if key in "downloadPath":
                downloadPath = path[key]
            if key in "webdriverPath":
                webdriverPath = path[key]
    return downloadPath, webdriverPath


def getConfig(pathToFile):
    data = jsonfile.read_json(pathToFile)
    try:
        if data["target"] is not None and data["user"] is not None:
            for key in data["target"]:
                username = key["username"]
                gmail = key["gmail"]
            for key in data["user"]:
                userGmail = key["userGmail"]
        else:
            return setupConfig(pathToFile)
        return username, gmail, userGmail
    except Exception as e:
        raise e


def writeSettings(download_path, webdriverPath):

    data = {}
    data["isFirstRun"] = False
    data["keyStatus"] = False
    data["path"] = {}
    path = data["path"]
    path["downloadPath"] = download_path
    path["webdriverPath"] = webdriverPath
    return data


def writeConfig(targetDict, userDict):

    data = {}
    data["target"] = []
    data["user"] = []
    data["target"].append(targetDict)
    data["user"].append(userDict)
    return data


def createKey(pathToFile):
    key = setting.Key()
    key_status = key.keyGen()
    data = jsonfile.read_json(pathToFile)
    data["keyStatus"] = key_status
    jsonfile.updata_json(pathToFile, data)
    userDict = {"userGmail": key.userGmailAcc}
    return userDict
