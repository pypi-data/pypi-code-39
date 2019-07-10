import pytest
import colorlog
import tempfile
import os.path
from entity_search.multitext.indices import *
from .helpers import *

logger = colorlog.getLogger(__name__)

def test_jaccard_index(dev_mm_multi_field_corpus, dev_binary_query_corpus):
    ji = JaccardFIndex(dev_mm_multi_field_corpus, weights)
    rs = ji.resolve_all(dev_binary_query_corpus)
    assert rs.matrix.getnnz() == 8
    assert rs.matrix[0,0] == pytest.approx(0.2750,.001)
    assert rs.matrix[1,0] == pytest.approx(0.6250,.001)
    assert rs.matrix[0,1] == pytest.approx(0.3000,.001)
    assert rs.matrix[1,1] == pytest.approx(0.2500,.001)
    assert rs.matrix[2,1] == pytest.approx(0.2500,.001)
    assert rs.matrix[3,1] == pytest.approx(0.5000,.001)
    assert rs.matrix[4,1] == pytest.approx(1.0000,.001)
    assert rs.matrix[5,1] == pytest.approx(0.3750,.001)

def test_cosine_index(dev_cosine_mm_multi_field_corpus, dev_cosine_query_corpus):
    ci = CosineFIndex(dev_cosine_mm_multi_field_corpus, weights)
    rs = ci.resolve_all(dev_cosine_query_corpus)
    assert rs.matrix.getnnz() == 8
    assert rs.matrix[0,0] == pytest.approx(0.4910,.001)
    assert rs.matrix[1,0] == pytest.approx(0.9536,.001)
    assert rs.matrix[0,1] == pytest.approx(0.1881,.001)
    assert rs.matrix[1,1] == pytest.approx(0.1836,.001)
    assert rs.matrix[2,1] == pytest.approx(0.2677,.001)
    assert rs.matrix[3,1] == pytest.approx(0.5177,.001)
    assert rs.matrix[4,1] == pytest.approx(1.0000,.001)
    assert rs.matrix[5,1] == pytest.approx(0.5303,.001)

def test_bm25_index(dev_bm25_mm_multi_field_corpus, dev_bm25_query_corpus):
    bi = BM25FIndex(dev_bm25_mm_multi_field_corpus, weights, k)
    rs = bi.resolve_all(dev_bm25_query_corpus)
    assert rs.matrix.getnnz() == 8
    assert rs.matrix[0,0] == pytest.approx(0.2329,.001)
    assert rs.matrix[1,0] == pytest.approx(0.3252,.001)
    # This values are negative because we have very few documents in the corpus
    assert rs.matrix[0,1] == pytest.approx(-0.3717,.001)
    assert rs.matrix[1,1] == pytest.approx(-0.2731,.001)
    assert rs.matrix[2,1] == pytest.approx(-0.2731,.001)
    assert rs.matrix[3,1] == pytest.approx(-0.3252,.001)
    assert rs.matrix[4,1] == pytest.approx(-0.5983,.001)
    assert rs.matrix[5,1] == pytest.approx(-0.3237,.001)

def test_save_load_index(dev_bm25_mm_multi_field_corpus):
    bi = BM25FIndex(dev_bm25_mm_multi_field_corpus, weights, k)
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_name = "{}/index".format(tmpdirname)
        bi.save(file_name)
        assert os.path.isfile(file_name)
        bi2 = BM25FIndex.load(file_name)
        assert len(bi2.corpus.fields) == len(bi.corpus.fields)
        assert len(bi2.weights) == len(bi.weights)
        assert len(bi2.indexes) == len(bi.indexes)
