import pytest
import colorlog
import tempfile
import re
from entity_search.run import *
from entity_search.diffusion import PureText
from entity_search.queries import Mapper, ReIndex
from entity_search.utilities import read_mapping_file, read_result_file
from .helpers import *

logger = colorlog.getLogger(__name__)

def test_execute_text_models(tes_jaccard_query_response_set, tes_transition, tes_re_index):
    with tempfile.TemporaryDirectory() as base_path:
        out_files = execute_text_models(tes_jaccard_query_response_set, tes_transition,
                tes_re_index, "test", base_path)
        pattern = "\\" + base_path + "/test_eqv_text*"
        assert len(out_files) == 1
        for out_file in out_files:
            assert re.match(pattern, out_file)
            result = read_result_file(out_file)
            assert result.shape == (393, 3)

def test_execute_lazy_models(tes_jaccard_query_response_set, tes_transition, tes_re_index):
    with tempfile.TemporaryDirectory() as base_path:
        out_files = execute_lazy_models(tes_jaccard_query_response_set, tes_transition,
                tes_re_index, 1, [0.5, 1.0],
                "test", base_path)
        pattern = "\\" + base_path + "/test_eqv_*"
        assert len(out_files) == 6
        for out_file in out_files:
            assert re.match(pattern, out_file)
            result = read_result_file(out_file)
            assert result.shape == (400, 3)

def test_execute_heat_lazy_models(tes_jaccard_query_response_set, tes_transition,
        tes_re_index):
    with tempfile.TemporaryDirectory() as base_path:
        out_files = execute_heat_lazy_models(tes_jaccard_query_response_set,
                tes_transition, tes_re_index, 1, [0.5, 1.0], [0.1, 0.2],
                "test", base_path)
        pattern = "\\" + base_path + "/test_eqv_*"
        assert len(out_files) == 8
        for out_file in out_files:
            assert re.match(pattern, out_file)
            result = read_result_file(out_file)
            assert result.shape == (400, 3)

def test_execute_all_models(tes_jaccard_query_response_set, tes_transition, tes_re_index):
    with tempfile.TemporaryDirectory() as base_path:
        out_files = execute_all_models(tes_jaccard_query_response_set,
                tes_transition, tes_re_index, 1, [0.1], [0.2],
                "test", base_path)
        pattern = "\\" + base_path + "/test_eqv_*"
        assert len(out_files) == 6
        for out_file in out_files:
            assert re.match(pattern, out_file)
            result = read_result_file(out_file)
            if re.match("\\" + base_path + "/test_eqv_text", out_file):
                assert result.shape == (393, 3)
            else:
                assert result.shape == (400, 3)

def test_execute_all_models_default(tes_jaccard_query_response_set, tes_transition,
        tes_re_index):
    with tempfile.TemporaryDirectory() as base_path:
        out_files = execute_all_models_default(tes_jaccard_query_response_set, tes_transition,
                tes_re_index, "test", base_path)
        pattern = "\\" + base_path + "/test_eqv_*"
        assert len(out_files) == 66
        for out_file in out_files:
            assert re.match(pattern, out_file)
            result = read_result_file(out_file)
            if re.match("\\" + base_path + "/test_eqv_text", out_file):
                assert result.shape == (393, 3)
            else:
                assert result.shape == (400, 3)
