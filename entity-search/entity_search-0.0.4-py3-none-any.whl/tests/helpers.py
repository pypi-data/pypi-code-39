import pytest
import gensim
import tempfile
import numpy as np
import pandas as pd
import scipy as sp
from entity_search.multitext.indices import *
from . import cfg

# Base path

@pytest.fixture(scope="session")
def dev_dataset_path():
    return "./etc"

@pytest.fixture(scope="session")
def tes_dataset_path():
    return "{}".format(cfg['testing']['folder'])

# Utility functions

def make_triple_set(_subject, _object, _predicate):
    return pd.DataFrame({'subject':_subject,'object':_object,'predicate':_predicate})

def write_mm_files(corpus, dictionary_file, field_files):
    corpus.dictionary.save_as_text(dictionary_file)
    for field, field_file in zip(corpus.fields, field_files):
        gensim.corpora.MmCorpus.serialize(field_file, field,
                id2word = corpus.dictionary)

def query_field_corpus(corpus, query_corpus, index, *args):
    result = query_multi_field_corpus([corpus], query_corpus, index, *args)
    return result[0]

def query_multi_field_corpus(fields, query_corpus, index, *args):
    I = index._index(fields)
    Q = index._prepare_queries(query_corpus, I[0].index.dtype)
    return index.resolve(I, Q)

def select_query_corpus(tes_binary_query_corpus, tes_cosine_query_corpus,
        tes_bm25_query_corpus, index):
    if index == JaccardFIndex:
        query_corpus = tes_binary_query_corpus
    elif index == CosineFIndex:
        query_corpus = tes_cosine_query_corpus
    elif index == BM25FIndex:
        query_corpus = tes_bm25_query_corpus
    else:
        raise RuntimeError('index={} not found'.format(index))
    return query_corpus

# Variables

fields = ["name", "attributes", "categories", "similar", "related"]
weights = [0.5, 0.2, 0.1, 0.1, 0.1]
Bs = [0.5, 0.6, 0.7, 0.8, 0.9]
k = 1.7
