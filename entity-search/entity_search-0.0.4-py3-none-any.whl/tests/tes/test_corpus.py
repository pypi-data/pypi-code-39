import pytest
import colorlog
import numpy as np
from entity_search.multitext.corpus import *
from .helpers import *

logger = colorlog.getLogger(__name__)

@pytest.mark.parametrize("corpus_class, fields", [(JsonGlobalField,()),
    (JsonSingleField, ("name",))])
def test_corpus(corpus_class, fields, tes_text_path, tes_dictionary):
    c = corpus_class(tes_text_path, *fields, dictionary = tes_dictionary)
    assert len(c) == 6221
    for doc in c:
        assert len(doc) > 0
        break

def test_json_multi_field_corpus(tes_text_path, tes_dictionary):
    pmfc = JsonMultiFieldCorpus(tes_text_path, fields, dictionary = tes_dictionary)
    assert len(pmfc.fields[0]) == 6221
    assert len(pmfc.fields) == 5
    for doc in pmfc.fields[0]:
        assert len(doc) > 0
        break

def test_mm_multi_field_corpus(tes_generate_mm_files):
    mmfc = MultiFieldCorpusABC.load_mm(tes_generate_mm_files)
    assert len(mmfc.fields[0]) == 6221
    assert len(mmfc.fields) == 5
    for doc in mmfc.fields[0]:
        assert len(doc) > 0
        break

def test_query_set(tes_queries_path, tes_dictionary):
    qs = QueryCorpus(tes_queries_path, tes_dictionary)
    assert len(qs.fields[0]) == 2
