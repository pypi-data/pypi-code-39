from .persister import Persister
import os
import pandas as pd
import pickle
import shutil
import unittest

class TestPersister(unittest.TestCase):
    def setUp(self):
        self.data_dir = os.path.dirname(__file__) + "/data"
        os.mkdir(self.data_dir)
    
    def test_no_implicit_overrides(self):
        p = Persister(self.data_dir)
        set1 = pd.DataFrame({"apples":[2, 3,3, 4]})
        self.assertRaises(KeyError, p.load, "somename")
        self.assertRaises(KeyError, p.overwrite, "somename", set1)

        p.save("somename", set1)
        self.assertRaises(KeyError, p.save, "somename", set1)

        df = p.load("somename")
        self.assertTrue(df.equals(set1))
        self.assertRaises(KeyError, p.load, "othername")
        self.assertRaises(KeyError, p.overwrite, "othername", set1)

        set2 = pd.DataFrame({"apples":[111, 3,3, 4]})
        p.overwrite("somename", set2)
        df = p.load("somename")
        self.assertFalse(df.equals(set1))
        self.assertTrue(df.equals(set2))


    def test_pickling(self):
        p = Persister(self.data_dir)
        set1 = pd.DataFrame({"apples":[2, 3,3, 4]})
        p.save("somename", set1)

        save_path = self.data_dir + "/persister.pkl"
        p.persist(save_path)
        q = Persister.load_from(save_path)
        df = q.load("somename")
        self.assertTrue(df.equals(set1))



    def tearDown(self):
        shutil.rmtree(self.data_dir)
    
