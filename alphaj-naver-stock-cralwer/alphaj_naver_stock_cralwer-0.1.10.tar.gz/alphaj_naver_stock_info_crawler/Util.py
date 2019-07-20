import json
import math

def floatOrZero(num):
    if num == None:
        return 0
    else:
        return float(num)


def convert_nan(val):
    if math.isnan(val):
        return -999999
    else:
        return val

def read_json(file_name):

    with open(file_name, 'r') as json_file:
        json_data = json.load(json_file)
        return json_data
