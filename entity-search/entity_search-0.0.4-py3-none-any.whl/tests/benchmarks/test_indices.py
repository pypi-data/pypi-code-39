import pytest
import colorlog
from entity_search.multitext.corpus import *
from entity_search.multitext.indices import *
from .helpers import *


@pytest.mark.parametrize("index, args", [(JaccardFIndex, []), (CosineFIndex, []), (BM25FIndex, [k])])
def test_index_creation(benchmark, index, args, tes_mm_multi_field_corpus):
    benchmark(index, tes_mm_multi_field_corpus, weights, *args)

@pytest.mark.parametrize("index, args", [(JaccardFIndex, []), (CosineFIndex, []), (BM25FIndex, [k])])
def test_index_similarity(benchmark, index, args, tes_mm_multi_field_corpus,
        tes_binary_query_corpus, tes_cosine_query_corpus, tes_bm25_query_corpus):
    query_corpus = select_query_corpus(tes_binary_query_corpus, tes_cosine_query_corpus,
            tes_bm25_query_corpus, index)
    fi = index(tes_mm_multi_field_corpus, weights, *args)
    benchmark(fi.resolve_all, query_corpus)
