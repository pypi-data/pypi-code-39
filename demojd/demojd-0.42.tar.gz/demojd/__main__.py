import sys
import getopt
import logging

from .scripts.hello import hello
from . import logger, console, debug

try:
    opts, args = getopt.getopt(sys.argv[1:], '-d', [])
except getopt.GetoptError as err:
    logger.error(err)
    logger.info(__doc__)
    sys.exit(2)

for opt, args in opts:
    if opt == '-d':
        debug = True

if debug:
    mode = logging.DEBUG
else:
    mode = logging.INFO

logger.setLevel(mode)
console.setLevel(mode)
logger.addHandler(console)

hello()
