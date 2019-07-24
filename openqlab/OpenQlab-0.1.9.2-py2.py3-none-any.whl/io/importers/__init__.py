import os
import glob
import importlib
from OpenQlab.io.importers import utils
from OpenQlab.io.importers.ascii import ASCII
from OpenQlab.io.importers.keysight_binary import KeysightBinary

# TODO maybe refactoring
IMPORTER_DIR = os.path.abspath(__file__)

IMPORTER_DIR = os.path.dirname(IMPORTER_DIR)

for fn in glob.glob(IMPORTER_DIR + "/*.py"):
    importer = utils.get_file_basename(fn)
    if importer in ('__init__', 'utils'):
        continue
    try:
        importer = importlib.import_module('OpenQlab.io.importers.' + importer, package='OpenQlab.io.importers')
    except ImportError as e:
        print(e)
        continue
