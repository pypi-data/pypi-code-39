import pytest
import colorlog
import gensim
from entity_search.multitext.corpus import *
from entity_search.multitext.similarities import *
from entity_search.multitext.indices import *
from .helpers import *

@pytest.mark.parametrize("index", [JaccardFIndex, CosineFIndex, BM25FIndex])
def test_single_field_similarity(benchmark, index, tes_mm_multi_field_corpus,
        tes_binary_query_corpus, tes_cosine_query_corpus, tes_bm25_query_corpus):
    query_corpus = select_query_corpus(tes_binary_query_corpus, tes_cosine_query_corpus,
            tes_bm25_query_corpus, index)
    sims = index._index([tes_mm_multi_field_corpus.fields[0]])
    queries = index._prepare_queries(query_corpus, sims[0].index.dtype)
    benchmark(sims[0].__getitem__, queries[0])

@pytest.mark.parametrize("index", [JaccardFIndex, CosineFIndex, BM25FIndex])
def test_multi_field_similarity(benchmark, index, tes_mm_multi_field_corpus,
        tes_binary_query_corpus, tes_cosine_query_corpus, tes_bm25_query_corpus):
    query_corpus = select_query_corpus(tes_binary_query_corpus, tes_cosine_query_corpus,
            tes_bm25_query_corpus, index)
    sims = index._index(tes_mm_multi_field_corpus.fields)
    queries = index._prepare_queries(query_corpus, sims[0].index.dtype)
    benchmark(index.resolve, sims, queries)

@pytest.mark.parametrize("index", [JaccardFIndex, CosineFIndex, BM25FIndex])
def test_similarity_creation(benchmark, index, tes_mm_multi_field_corpus):
    benchmark(index._index, tes_mm_multi_field_corpus.fields)
