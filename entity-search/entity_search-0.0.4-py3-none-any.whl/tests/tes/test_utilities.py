import pytest
import colorlog
import tempfile
import os
from entity_search.utilities import *
from .helpers import *

logger = colorlog.getLogger(__name__)

# Helpers

@pytest.fixture
def generate_query_result():
    return pd.DataFrame({'query':['q1','q2'],'entity':['e1','e2'],
        'rank':[1,2],'score':[1.0,0.9]})

def test_read_trec_gt_file(tes_qrels_path):
    df = read_trec_gt_file(tes_qrels_path)
    assert df.size == 103*3

def test_read_trec_mapping_file(tes_mapping_path):
    df = read_trec_mapping_file(tes_mapping_path)
    assert df.size == 6221

def test_write_trec_ranking_file(generate_query_result):
    file_path = tempfile.mkstemp()[1]
    try:
        write_trec_ranking_file(generate_query_result, file_path)
        with open(file_path) as f:
            content = f.readlines()
    finally:
        os.remove(file_path)
    assert content[0] == 'q1 Q0 e1 1 1.0 katz\n'
    assert content[1] == 'q2 Q0 e2 2 0.9 katz\n'

def test_read_adjacency_file(tes_adjacency_path):
    matrix = read_adjacency_file(tes_adjacency_path)
    assert matrix.shape == (6221, 6221, 115)
    assert matrix.nnz == 6708
