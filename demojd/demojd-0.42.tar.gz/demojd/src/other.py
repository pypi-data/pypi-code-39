import json
import os

import logging
logger = logging.getLogger(__name__)

from . import data_fpath
from .general import hello as hello_general

def hello():
    with open(data_fpath, 'r') as f:
        guest_list = json.load(f)
    for each in guest_list["others"]:
        hello_general('Hi from ' + each + '!')
    logger.debug('Hi from ' + __name__ + '(debug message)')
