import logging
import os

debug = False

console = logging.StreamHandler()
logger = logging.getLogger(__name__)

data_fpath = __path__[0] + os.sep + 'data' + os.sep + 'others.json'
