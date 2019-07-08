import json

def JsonReader(filePath):
    with open(filePath) as json_file:
        return json.load(json_file)
