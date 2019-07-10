import pytest
import colorlog
import gensim
import numpy as np
import scipy as sp
from entity_search.multitext.corpus import *
from entity_search.multitext.similarities import *
from entity_search.multitext.indices import *
from .helpers import *

logger = colorlog.getLogger(__name__)

@pytest.mark.parametrize("index, args", [(JaccardFIndex, []), (CosineFIndex, []),
    (BM25FIndex, (Bs,))])
def test_global_corpus_similarity(tes_global_field, tes_query_corpus, index, args):
    score = query_field_corpus(tes_global_field, tes_query_corpus, index, *args)
    assert score.getnnz() > 0

@pytest.mark.parametrize("index, args", [(JaccardFIndex, []), (CosineFIndex, []),
    (BM25FIndex, (Bs,))])
def test_field_corpus_similarity(tes_single_field, tes_query_corpus, index, args):
    score = query_field_corpus(tes_single_field, tes_query_corpus, index, *args)
    assert score.getnnz() > 0

@pytest.mark.parametrize("index", [JaccardFIndex, CosineFIndex, BM25FIndex])
def test_json_multi_field_corpus_similarity(tes_json_multi_field_corpus,
        tes_binary_query_corpus, tes_cosine_query_corpus, tes_bm25_query_corpus,
        index):
    query_corpus = select_query_corpus(tes_binary_query_corpus, tes_cosine_query_corpus,
            tes_bm25_query_corpus, index)
    scores = query_multi_field_corpus(tes_json_multi_field_corpus.fields, query_corpus,
            index)
    assert scores[0].getnnz() > 0 # name
    assert scores[1].getnnz() > 0 # attributes

@pytest.mark.parametrize("index", [JaccardFIndex, CosineFIndex, BM25FIndex])
def test_mm_multi_field_corpus_similarity(tes_mm_multi_field_corpus,
        tes_binary_query_corpus, tes_cosine_query_corpus, tes_bm25_query_corpus,
        index):
    query_corpus = select_query_corpus(tes_binary_query_corpus, tes_cosine_query_corpus,
            tes_bm25_query_corpus, index)
    scores = query_multi_field_corpus(tes_mm_multi_field_corpus.fields, query_corpus, index)
    assert scores[0].getnnz() > 0 # name
    assert scores[1].getnnz() > 0 # attributes
