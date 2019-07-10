import pytest
import colorlog
import gensim
from functools import partial
from entity_search.multitext.corpus import *
from entity_search.multitext.similarities import *
from entity_search.multitext.indices import *
from .helpers import *

logger = colorlog.getLogger(__name__)

# Tests

def test_global_corpus_jaccard(dev_binary_global_field, dev_binary_query_corpus):
    score = query_field_corpus(dev_binary_global_field, dev_binary_query_corpus, JaccardFIndex)
    assert score.getnnz() == 8
    assert score[0,0] == pytest.approx(0.2000,.001)
    assert score[1,0] == pytest.approx(0.5000,.001)
    assert score[0,1] == pytest.approx(0.4000,.001)
    assert score[1,1] == pytest.approx(0.3333,.001)
    assert score[2,1] == pytest.approx(0.3333,.001)
    assert score[3,1] == pytest.approx(0.3333,.001)
    assert score[4,1] == pytest.approx(1.0000,.001)
    assert score[5,1] == pytest.approx(0.5000,.001)

def test_multi_field_corpus_jaccard(dev_binary_json_multi_field_corpus,
        dev_binary_query_corpus):
    scores = query_multi_field_corpus(dev_binary_json_multi_field_corpus.fields,
            dev_binary_query_corpus, JaccardFIndex)
    assert scores[0].getnnz() == 8
    assert scores[0][0,0] == pytest.approx(0.2000,.001)
    assert scores[0][1,0] == pytest.approx(0.5000,.001)
    assert scores[0][0,1] == pytest.approx(0.4000,.001)
    assert scores[0][1,1] == pytest.approx(0.3333,.001)
    assert scores[0][2,1] == pytest.approx(0.3333,.001)
    assert scores[0][3,1] == pytest.approx(0.3333,.001)
    assert scores[0][4,1] == pytest.approx(1.0000,.001)
    assert scores[0][5,1] == pytest.approx(0.5000,.001)
    assert scores[1].getnnz() == 4
    assert scores[1][0,0] == pytest.approx(0.5000,.001)
    assert scores[1][1,0] == pytest.approx(1.0000,.001)
    assert scores[1][3,1] == pytest.approx(1.0000,.001)
    assert scores[1][4,1] == pytest.approx(1.0000,.001)

def test_global_corpus_cosine(dev_cosine_global_field, dev_cosine_query_corpus):
    score = query_field_corpus(dev_cosine_global_field, dev_cosine_query_corpus, CosineFIndex)
    assert score.getnnz() == 8
    assert score[0,0] == pytest.approx(0.5113,.001)
    assert score[1,0] == pytest.approx(0.9833,.001)
    assert score[0,1] == pytest.approx(0.1333,.001)
    assert score[1,1] == pytest.approx(0.1283,.001)
    assert score[2,1] == pytest.approx(0.1984,.001)
    assert score[3,1] == pytest.approx(0.5375,.001)
    assert score[4,1] == pytest.approx(0.9486,.001)
    assert score[5,1] == pytest.approx(0.7071,.001)

def test_multi_field_corpus_cosine(dev_cosine_json_multi_field_corpus,
        dev_cosine_query_corpus):
    scores = query_multi_field_corpus(dev_cosine_json_multi_field_corpus.fields,
        dev_cosine_query_corpus, CosineFIndex)
    assert scores[0].getnnz() == 8
    assert scores[0][0,0] == pytest.approx(0.4805,.001)
    assert scores[0][1,0] == pytest.approx(0.9381,.001)
    assert scores[0][0,1] == pytest.approx(0.2508,.001)
    assert scores[0][1,1] == pytest.approx(0.2448,.001)
    assert scores[0][2,1] == pytest.approx(0.3570,.001)
    assert scores[0][3,1] == pytest.approx(0.3570,.001)
    assert scores[0][4,1] == pytest.approx(0.9999,.001)
    assert scores[0][5,1] == pytest.approx(0.7071,.001)
    assert scores[1].getnnz() == 4
    assert scores[1][0,0] == pytest.approx(0.5227,.001)
    assert scores[1][1,0] == pytest.approx(1.0000,.001)
    assert scores[1][3,1] == pytest.approx(1.0000,.001)
    assert scores[1][4,1] == pytest.approx(1.0000,.001)

def test_global_corpus_bm25(dev_bm25_global_field, dev_bm25_query_corpus):
    scores = query_field_corpus(dev_bm25_global_field, dev_bm25_query_corpus, BM25FIndex)
    assert scores.getnnz() == 10
    assert scores[1,0] == pytest.approx(2.1538,.001)
    assert scores[0,0] == pytest.approx(1.2727,.001)
    assert scores[0,2] == pytest.approx(0.6363,.001)
    assert scores[0,1] == pytest.approx(0.6363,.001)
    assert scores[1,1] == pytest.approx(1.0769,.001)
    assert scores[2,1] == pytest.approx(1.0769,.001)
    assert scores[3,2] == pytest.approx(2.1538,.001)
    assert scores[4,1] == pytest.approx(1.0769,.001)
    assert scores[4,2] == pytest.approx(2.1538,.001)
    assert scores[5,2] == pytest.approx(1.4000,.001)

def test_multi_field_corpus_bm25(dev_bm25_json_multi_field_corpus, dev_bm25_query_corpus):
    scores = query_multi_field_corpus(dev_bm25_json_multi_field_corpus.fields,
            dev_bm25_query_corpus, BM25FIndex)
    assert scores[0].getnnz() == 10
    assert scores[0][1,0] == pytest.approx(1.0769,.001)
    assert scores[0][0,0] == pytest.approx(0.6363,.001)
    assert scores[0][0,1] == pytest.approx(0.6363,.001)
    assert scores[0][0,2] == pytest.approx(0.6363,.001)
    assert scores[0][1,1] == pytest.approx(1.0769,.001)
    assert scores[0][2,1] == pytest.approx(1.0769,.001)
    assert scores[0][3,2] == pytest.approx(1.0769,.001)
    assert scores[0][4,1] == pytest.approx(1.0769,.001)
    assert scores[0][4,2] == pytest.approx(1.0769,.001)
    assert scores[0][5,2] == pytest.approx(1.4000,.001)
    assert scores[1].getnnz() == 4
    assert scores[1][1,0] == pytest.approx(1.0,.001)
    assert scores[1][0,0] == pytest.approx(0.6666,.001)
    assert scores[1][3,2] == pytest.approx(1.0000,.001)
    assert scores[1][4,2] == pytest.approx(1.0000,.001)
