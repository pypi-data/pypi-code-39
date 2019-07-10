import unittest
import colorlog
import tempfile
import os
from ..utilities import *
from . import cfg

logger = colorlog.getLogger(__name__)

class test_inputs_output(unittest.TestCase):
    def setUp(self):
        pass

    def test_read_trec_gt_file(self):
        df = read_trec_gt_file('etc/qrels.txt')
        self.assertEqual(df.size, 103*3)

    def test_read_trec_mapping_file(self):
        df = read_trec_mapping_file('etc/mapping_nodes')
        self.assertEqual(df.size, 6603)

    def test_write_trec_ranking_file(self):
        df = pd.DataFrame({'query':['q1','q2'],'entity':['e1','e2'],
            'rank':[1,2],'score':[1.0,0.9]})
        file_path = tempfile.mkstemp()[1]
        try:
            write_trec_ranking_file(df, file_path)
            with open(file_path) as f:
                content = f.readlines()
        finally:
            os.remove(file_path)
        self.assertEqual(content[0], 'q1 Q0 e1 1 1.0 katz\n')
        self.assertEqual(content[1], 'q2 Q0 e2 2 0.9 katz\n')
            
        
