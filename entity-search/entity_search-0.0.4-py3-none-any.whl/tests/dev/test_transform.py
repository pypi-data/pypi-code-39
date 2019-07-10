import pytest
import colorlog
import tempfile
import os
from functools import partial
from entity_search.multitext.indices import JaccardFIndex
from entity_search.multitext.transform import *
from .helpers import *

logger = colorlog.getLogger(__name__)

def test_transform_query_corpus_binary(dev_json_multi_field_corpus, dev_query_corpus):
    funcs =[ partial(JaccardFIndex._tfidf_query_model_kargs) for _ in
        dev_json_multi_field_corpus.fields ]
    tf = TransformedCorpus(dev_query_corpus, dev_json_multi_field_corpus, funcs)
    queries = [doc for doc in tf.fields[0]]
    assert len(queries) == 2
    assert queries[0] == [(1, 1.0)]
    assert queries[1] == [(2, 1.0), (4, 1.0)]

def test_transform_query_corpus_cosine(dev_json_multi_field_corpus, dev_query_corpus):
    funcs =[ partial(CosineFIndex._tfidf_query_model_kargs) for _ in
        dev_json_multi_field_corpus.fields ]
    tf = TransformedCorpus(dev_query_corpus, dev_json_multi_field_corpus, funcs)
    queries = [doc for doc in tf.fields[0]]
    assert len(queries) == 2
    assert queries[0] == [(1, 1.0)]
    assert queries[1][0][1] == pytest.approx(0.7071, 0.001)
    assert queries[1][1][1] == pytest.approx(0.7071, 0.001)

def test_transform_query_corpus_bm25(dev_json_multi_field_corpus, dev_query_corpus):
    funcs =[ partial(BM25FIndex._tfidf_query_model_kargs) for _ in
        dev_json_multi_field_corpus.fields ]
    tc = TransformedCorpus(dev_query_corpus, dev_json_multi_field_corpus, funcs)
    queries0 = [doc for doc in tc.fields[0]]
    assert len(queries0) == 2
    assert queries0[0] == [(1, 1.0)]
    assert queries0[1] == [(2, 1.0), (4, 1.0)]
    queries1 = [doc for doc in tc.fields[1]]
    assert len(queries1) == 2
    assert queries1[0] == [(1, 1.0)]
    assert queries1[1] == [(2, 0.0), (4, 1.0)]

def test_transform_query_corpus_to_mm(dev_json_multi_field_corpus, dev_query_corpus):
    funcs =[ partial(JaccardFIndex._tfidf_query_model_kargs) for _ in
        dev_json_multi_field_corpus.fields ]
    tf = TransformedCorpus(dev_query_corpus, dev_json_multi_field_corpus, funcs)
    assert len(tf.fields) == 2
    temp_dir = tempfile.mkdtemp()
    temp_file_base = "{}/{}".format(temp_dir, "my_test")
    temp_files = tf.save_as_mm(temp_file_base)
    tf = QueryCorpus.load_mm(temp_file_base)
    assert len(tf.fields) == 2
    queries0 = [ doc for doc in tf.fields[0] ]
    assert len(queries0) == 2
    assert queries0[0] == [(1, 1.0)]
    assert queries0[1] == [(2, 1.0), (4, 1.0)]
    queries1 = [ doc for doc in tf.fields[1] ]
    assert len(queries1) == 2
    assert queries1[0] == [(1, 1.0)]
    assert queries1[1] == [(4, 1.0)]
    ids = tf.ids
    assert len(ids) == 2
    assert ids[0] == "SemSearch_ES-1"
    assert ids[1] == "SemSearch_LS-2"
    lengths = tf.lengths
    assert len(lengths) == 2
    assert lengths[0] == 1
    assert lengths[1] == 2
    list(map(os.remove, temp_files))

def test_transform_single_field(dev_single_field):
    tf = TransformedField(dev_single_field, dev_single_field,
            JaccardFIndex._tfidf_model_kargs)
    docs = [ doc for doc in tf ]
    assert len(docs) == 6
    assert docs[0] == [(0, 1.0), (1, 1.0), (2, 1.0), (3, 1.0), (4, 1.0)]
    assert docs[1] == [(1, 1.0), (2, 1.0)]
    assert docs[2] == [(2, 1.0), (3, 1.0)]
    assert docs[3] == [(3, 1.0), (4, 1.0)]
    assert docs[4] == [(2, 1.0), (4, 1.0)]
    assert docs[5] == [(4, 1.0)]

def test_transform_multi_field_corpus(dev_json_multi_field_corpus):
    funcs =[ partial(JaccardFIndex._tfidf_model_kargs) for _ in
        dev_json_multi_field_corpus.fields ]
    tf = TransformedCorpus(dev_json_multi_field_corpus, dev_json_multi_field_corpus, funcs)
    docs0 = [ doc for doc in tf.fields[0]]
    assert len(docs0) == 6
    assert docs0[0] == [(0, 1.0), (1, 1.0), (2, 1.0), (3, 1.0), (4, 1.0)]
    assert docs0[1] == [(1, 1.0), (2, 1.0)]
    assert docs0[2] == [(2, 1.0), (3, 1.0)]
    assert docs0[3] == [(3, 1.0), (4, 1.0)]
    assert docs0[4] == [(2, 1.0), (4, 1.0)]
    assert docs0[5] == [(4, 1.0)]
    docs1 = [ doc for doc in tf.fields[1]]
    assert len(docs1) == 6
    assert docs1[0] == [(0, 1.0), (1, 1.0)]
    assert docs1[1] == [(1, 1.0)]
    assert docs1[2] == [(3, 1.0)]
    assert docs1[3] == [(4, 1.0)]
    assert docs1[4] == [(4, 1.0)]
    assert docs1[5] == []

def test_transform_multi_field_corpus_to_mm(dev_json_multi_field_corpus):
    funcs =[ partial(JaccardFIndex._tfidf_model_kargs) for _ in
        dev_json_multi_field_corpus.fields ]
    tc = TransformedCorpus(dev_json_multi_field_corpus, dev_json_multi_field_corpus, funcs)
    temp_dir = tempfile.mkdtemp()
    temp_file_base = "{}/{}".format(temp_dir, "my_test")
    temp_files = tc.save_as_mm(temp_file_base)
    tc = MultiFieldCorpusABC.load_mm(temp_file_base)
    docs0 = [ doc for doc in tc.fields[0]]
    assert len(docs0) == 6
    assert docs0[0] == [(0, 1.0), (1, 1.0), (2, 1.0), (3, 1.0), (4, 1.0)]
    assert docs0[1] == [(1, 1.0), (2, 1.0)]
    assert docs0[2] == [(2, 1.0), (3, 1.0)]
    assert docs0[3] == [(3, 1.0), (4, 1.0)]
    assert docs0[4] == [(2, 1.0), (4, 1.0)]
    assert docs0[5] == [(4, 1.0)]
    docs1 = [ doc for doc in tc.fields[1]]
    assert len(docs1) == 6
    assert docs1[0] == [(0, 1.0), (1, 1.0)]
    assert docs1[1] == [(1, 1.0)]
    assert docs1[2] == [(3, 1.0)]
    assert docs1[3] == [(4, 1.0)]
    assert docs1[4] == [(4, 1.0)]
    assert docs1[5] == []
    list(map(os.remove, temp_files))
