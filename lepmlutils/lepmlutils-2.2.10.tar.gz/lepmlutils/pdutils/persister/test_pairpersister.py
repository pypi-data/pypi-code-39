from .pairpersister import PairPersister
import os
import pandas as pd
import pickle
import shutil
import unittest

class TestPairPersister(unittest.TestCase):
    def setUp(self):
        self.data_dir = os.path.dirname(__file__) + "/data"
        os.mkdir(self.data_dir)
    
    def test_no_implicit_overrides(self):
        p = PairPersister(self.data_dir)
        trn = pd.DataFrame({"apples": [2, 3, 4, 5]})
        tst = pd.DataFrame({"apples": [2, 6, 47]})
        self.assertRaises(KeyError, p.overwrite_pair, "apples", trn, tst)
        self.assertRaises(KeyError, p.load_pair, "apples")

        p.save_pair("apples", trn, tst)
        self.assertRaises(KeyError, p.save_pair, "apples", trn, tst)

        trn2, tst2 = p.load_pair("apples")
        self.assertTrue(trn2.equals(trn))
        self.assertTrue(tst2.equals(tst))

        trn3 = pd.DataFrame({"apples": [2, 777, 4, 5]})
        tst3 = pd.DataFrame({"apples": [2, 611, 47]})

        p.overwrite_pair("apples", trn, tst)
        trn2, tst2 = p.load_pair("apples")
        self.assertFalse(trn2.equals(trn3))
        self.assertFalse(tst2.equals(tst3))

        

    def tearDown(self):
        shutil.rmtree(self.data_dir)
    
