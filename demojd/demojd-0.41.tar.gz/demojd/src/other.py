import json
import os

from . import logger, data_fpath
from . import hello as hello_main

def hello():
    with open(data_fpath, 'r') as f:
        guest_list = json.load(f)
    for each in guest_list["others"]:
        hello_main('Hi from ' + each + '!')
    logger.debug('Hi from ' + __name__ + '(debug message)')
