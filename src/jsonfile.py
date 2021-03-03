import json


def write_json(pathToFile, data):
    with open(pathToFile, "w") as outFile:
        json.dump(data, outFile)


def read_json(pathToFile):
    with open(pathToFile, "r") as readFile:
        data = json.load(readFile)
        return data

def updata_json(pathToFile, updataData):
    write_json(pathToFile, updataData)


