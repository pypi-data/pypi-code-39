import logging
import os

mode = None

if __debug__:
    mode = logging.DEBUG
else:
    mode = logging.INFO

console = logging.StreamHandler()
console.setLevel(mode)

logger = logging.getLogger(__name__)
logger.setLevel(mode)

logger.addHandler(console)

def hello(msg):
    logger.info(msg)

data_fpath = __path__[0] + os.sep + 'data' + os.sep + 'others.json'
