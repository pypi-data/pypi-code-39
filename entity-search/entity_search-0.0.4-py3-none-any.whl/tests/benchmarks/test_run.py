import pytest
import colorlog
from entity_search.run import *
from .helpers import *

@pytest.mark.parametrize("num_processors", [1,2,4,8])
def test_execute_all_models(benchmark, tes_transition, tes_jaccard_query_response_set,
        tes_re_index, num_processors):
    with tempfile.TemporaryDirectory() as base_path:
        benchmark(execute_all_models_default, tes_jaccard_query_response_set,
            tes_transition, tes_re_index, "test", base_path, num_processors)
