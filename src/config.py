import os

import setting
import jsonfile

appname = "WhatsMail"
appauthor = "jamestansx"
dirs = ""
userData_json = ""
userConfig_json = ""


def isFirstRun():
    global dirs
    global userData_json
    dirs = setting.getDirs(appname, appauthor)
    userData_json = os.path.join(dirs["userData"], "data.json")
    if os.path.isfile(userData_json):
        return getSettings(userData_json)
    else:
        return setupSetting(userData_json)


def isConfig():
    global userConfig_json
    userConfig_json = os.path.join(dirs["userConfig"], "config.json")
    if os.path.isfile(userConfig_json):
        return getConfig(userConfig_json)
    else:
        return setupConfig(userConfig_json)


def setupSetting(pathToFile):
    download_path = input("Please enter the download path: ")
    webdriverPath = input("Please enter the path to the Chrome webdriver: ")
    chromedataPath = getChomedataPath()
    pathDict = {
        "downloadPath": download_path,
        "webdriverPath": webdriverPath,
        "chromedataPath": chromedataPath,
    }
    jsonfile.write_json(pathToFile, writeSettings(pathDict))
    return download_path, webdriverPath, chromedataPath, True


def getChomedataPath():
    response = input("Chrome profile path: \nDefault path (y/n): ")
    if response.strip().lower() in {"y", "yes"}:
        userCachedProfile = os.path.join(dirs["userCache"], "websession")
        os.makedirs(userCachedProfile, exist_ok=True)
        return userCachedProfile
    if response.strip().lower() in {"n", "no"}:
        chromedataPath = input("Please enter the path to the Chrome appdata: ")
        return chromedataPath


def setupConfig(pathToFile):
    target = setting.target()
    username, gmail = target.newTarget()
    targetDict = {"username": username, "gmail": gmail}
    userDict = createKey()
    jsonfile.write_json(pathToFile, writeConfig(targetDict, userDict))
    return username, gmail, userDict["userGmail"]


def getSettings(pathToFile):
    data = jsonfile.read_json(pathToFile)
    try:
        if data["isFirstRun"] is not False:
            return setupSetting(pathToFile)
        if data["keyStatus"] is False:
            global userDict
            userDict = createKey()
            jsonfile.write_json(userConfig_json, writeConfig(None, userDict))
    except Exception as e:
        raise e
    path = data["path"]
    downloadPath, webdriverPath, chromedataPath = None, None, None
    for key in path:
        if os.path.isfile(path[key]) is True:
            if key in "webdriverPath":
                webdriverPath = path[key]
        if os.path.isdir(path[key]) is True:
            if key in "downloadPath":
                downloadPath = path[key]
            if key in "chromedataPath":
                chromedataPath = path[key]
    return downloadPath, webdriverPath, chromedataPath, data["isFirstRun"]


def getConfig(pathToFile):
    data = jsonfile.read_json(pathToFile)
    try:
        if bool(data["target"]) and bool(data["user"]):
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


def writeSettings(pathDict):

    data = {}
    data["isFirstRun"] = True
    data["keyStatus"] = False
    data["path"] = pathDict
    return data


def writeConfig(targetDict=None, userDict=None):

    data = {}
    data["user"] = []
    data["target"] = []
    if userDict is not None:
        data["user"].append(userDict)
    if targetDict is not None:
        data["target"].append(targetDict)
    return data


def createKey():
    key = setting.Key()
    key_status = key.keyGen()
    data = jsonfile.read_json(userData_json)
    data["keyStatus"] = key_status
    jsonfile.updata_json(userData_json, data)
    userDict = {"userGmail": key.userGmailAcc}
    return userDict
