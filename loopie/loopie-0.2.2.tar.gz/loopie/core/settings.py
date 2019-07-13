'''
Created on Tuesday 03/07/2018

@author: yaztown
'''

# from datetime import time, timedelta

# import json
from loopie.core.json import loads

def load_settings_from_file(filename='settings/loopie_settings.json'):
    with open(filename, 'r') as f:
        data = f.read()
    return loads(data)
