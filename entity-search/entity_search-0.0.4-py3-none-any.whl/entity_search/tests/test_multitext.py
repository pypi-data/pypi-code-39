import unittest
import colorlog
from ..multitext import *
from . import cfg

logger = colorlog.getLogger(__name__)

fields = ["name", "attributes", "categories", "similar", "related"]

class test_global_corpus(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        print(cfg['development']['folder'])
        #GlobalCorpus(cfg['development']['folder'], fields)
