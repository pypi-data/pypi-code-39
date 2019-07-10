import pytest
import colorlog
import gensim
import tempfile
import os.path
from entity_search.multitext.corpus import *
from entity_search.multitext.similarities import *
from entity_search.multitext.indices import *
from .helpers import *

logger = colorlog.getLogger(__name__)

@pytest.mark.parametrize("index,args", [(JaccardFIndex, []), (CosineFIndex, []),
    (BM25FIndex, [k] )])
def test_json_multi_index(tes_json_multi_field_corpus, tes_binary_query_corpus,
        tes_cosine_query_corpus, tes_bm25_query_corpus, index, args):
    query_corpus = select_query_corpus(tes_binary_query_corpus, tes_cosine_query_corpus,
            tes_bm25_query_corpus, index)
    fi = index(tes_json_multi_field_corpus, weights, *args)
    qrs = fi.resolve_all(query_corpus)
    assert qrs.matrix.getnnz() > 0

@pytest.mark.parametrize("index,args", [(JaccardFIndex, []), (CosineFIndex, []),
    (BM25FIndex, [k] )])
def test_mm_multi_index(tes_mm_multi_field_corpus, tes_binary_query_corpus,
        tes_cosine_query_corpus, tes_bm25_query_corpus, index, args):
    query_corpus = select_query_corpus(tes_binary_query_corpus, tes_cosine_query_corpus,
            tes_bm25_query_corpus, index)
    fi = index(tes_mm_multi_field_corpus, weights, *args)
    qrs = fi.resolve_all(query_corpus)
    assert qrs.matrix.getnnz() > 0

@pytest.mark.parametrize("index,args", [(JaccardFIndex, []), (CosineFIndex, []),
    (BM25FIndex, [k] )])
def test_save_load_index(tes_mm_multi_field_corpus, index, args):
    fi = index(tes_mm_multi_field_corpus, weights, *args)
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_name = "{}/index".format(tmpdirname)
        fi.save(file_name)
        assert os.path.isfile(file_name)
        fi2 = index.load(file_name)
        assert len(fi2.corpus.fields) == len(fi.corpus.fields)
        assert len(fi2.weights) == len(fi.weights)
        assert len(fi2.indexes) == len(fi.indexes)
