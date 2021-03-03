import os

import setting
import jsonfile


def isFirstRun():
    appname = "WhatsMail"
    appauthor = "jamestansx"
    dirs = setting.getDirs(appname, appauthor)
    userData_json = os.path.join(dirs["userData"], "data.json")
    if os.path.isfile(userData_json):
        return getSettings(userData_json)
    else:
        downloadPath = input("Please enter the download path: ")
        webdriverPath = input("Please enter the path to the Chrome webdriver: ")
        jsonfile.write_json(userData_json, writeSettings(downloadPath, webdriverPath))
        return downloadPath, webdriverPath


def getSettings(pathToFile):
    data = jsonfile.read_json(pathToFile)
    if data["isFirstRun"] is not False:
        pass
    path = data["path"]
    for key in path:
        if os.path.isfile(path[key]) is True:
            if key in "downloadPath":
                downloadPath = key
            if key in "webdriverPath":
                webdriverPath = key
    return downloadPath, webdriverPath

def writeSettings(downloadPath, webdriverPath):
    data = {}
    data['isFirstRun'] = False
    data['path'] = {}
    path = data['path']
    path['downloadPath'] = downloadPath
    path['webdriverPath'] = webdriverPath
    return data
