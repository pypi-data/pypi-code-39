import pytest
import colorlog
from entity_search.results import *
from .helpers import *

logger = colorlog.getLogger(__name__)

def test_read_trec_files(dev_trec_files, dev_groundtruth_path):
    base_path, prefix, files = dev_trec_files
    results = TrecResults(base_path, prefix, dev_groundtruth_path)
    clas = results.classify_by_algorithm()
    table, cap = results.get_ndcg_lazy_vs_kernel_table(clas, 'prank', 0)
    output = results.find_best_by_diffusion(clas, 0)
    assert len(output) == 4
    #for out in output:
    #    print("Best configuration for {} is {}, when {} and {}".format(
    #            out[3], out[0], out[1], out[2]))
    output = results.find_best_by_query_type(clas, 0)
    assert len(output) == 2
    #for out in output:
    #    print("Best configuration for {} is {}, when {} and {} and {}".format(
    #        out[4], out[0], out[1], out[2], out[3]))
