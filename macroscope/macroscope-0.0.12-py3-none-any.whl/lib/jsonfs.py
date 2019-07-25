# Standard library
import json


def getJsonFromFile(filePath: str):
    fileConfig = None

    with open(filePath, 'r') as json_file:
        fileConfig = json.load(json_file)

    return fileConfig


def writeJsonToFile(filePath, jsonToWrite):
    with open(filePath, 'w+') as outfile:
        json.dump(jsonToWrite, outfile, indent=4)
