import pytest
import colorlog
from entity_search.results import *
from .helpers import *

logger = colorlog.getLogger(__name__)

def test_read_trec_files(tes_trec_files, tes_groundtruth_path):
    base_path, prefix, files = tes_trec_files
    results = TrecResults(base_path, prefix, tes_groundtruth_path)
    clas = results.classify_by_algorithm()
    table, cap = results.get_ndcg_lazy_vs_kernel_table(clas, 'prank', 0)
    output = results.find_best_by_diffusion(clas, 0)
    assert len(output) == 4
    output = results.find_best_by_query_type(clas, 0)
    assert len(output) == 1
