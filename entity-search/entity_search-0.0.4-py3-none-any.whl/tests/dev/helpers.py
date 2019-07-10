import pytest
import gensim
import tempfile
import os
import numpy as np
from functools import partial
from entity_search.adjacency import EqualWeight, Compressor, Transition
from entity_search.utilities import triple_set_to_sparse_matrix, read_adjacency_file, read_mapping_file
from entity_search.multitext.corpus import *
from entity_search.multitext.indices import JaccardFIndex
from entity_search.multitext.transform import *
from entity_search.queries import Mapper, ReIndex
from entity_search.run import execute_all_models_default
from ..helpers import *

# File Paths

@pytest.fixture(scope="session")
def dev_text_path(dev_dataset_path):
    return "{}/{}".format(dev_dataset_path, "dev-text.json")

@pytest.fixture(scope="session")
def dev_queries_path(dev_dataset_path):
    return "{}/{}".format(dev_dataset_path, "dev-queries.csv")

@pytest.fixture(scope="session")
def dev_mapping_path(dev_dataset_path):
    return "{}/{}".format(dev_dataset_path, "dev-mapping.csv")

@pytest.fixture(scope="session")
def dev_adjacency_path(dev_dataset_path):
    return "{}/{}".format(dev_dataset_path, "dev-adjacency.csv")

@pytest.fixture(scope="session")
def dev_groundtruth_path(dev_dataset_path):
    return "{}/{}".format(dev_dataset_path, "dev-qrels.txt")

# Objects

@pytest.fixture(scope="session")
def dev_transition(dev_adjacency_path):
    return Transition(Compressor(EqualWeight(read_adjacency_file(dev_adjacency_path))))

@pytest.fixture(scope="session")
def dev_global_field(dev_text_path):
    return JsonGlobalField(dev_text_path)

@pytest.fixture(scope="session")
def dev_binary_global_field(dev_global_field):
    return TransformedField(dev_global_field, dev_global_field,
            JaccardFIndex._tfidf_model_kargs)

@pytest.fixture(scope="session")
def dev_cosine_global_field(dev_global_field):
    return TransformedField(dev_global_field, dev_global_field,
            CosineFIndex._tfidf_model_kargs)

@pytest.fixture(scope="session")
def dev_bm25_global_field(dev_global_field):
    return TransformedField(dev_global_field, dev_global_field,
            partial(BM25FIndex._tfidf_model_kargs, slope = Bs[0]))

@pytest.fixture(scope = "session")
def dev_single_field(dev_text_path, dev_dictionary):
    return JsonSingleField(dev_text_path, fields[0], dev_dictionary)

@pytest.fixture(scope = "session")
def dev_dictionary(dev_global_field):
    return dev_global_field.dictionary

@pytest.fixture(scope = "session")
def dev_query_corpus(dev_queries_path, dev_dictionary):
    return QueryCorpus(dev_queries_path, dev_dictionary)

@pytest.fixture(scope = "session")
def dev_binary_query_corpus(dev_query_corpus, dev_json_multi_field_corpus):
    funcs =[ partial(JaccardFIndex._tfidf_query_model_kargs) for _ in
        dev_json_multi_field_corpus.fields ]
    return TransformedCorpus(dev_query_corpus, dev_json_multi_field_corpus, funcs)

@pytest.fixture(scope = "session")
def dev_cosine_query_corpus(dev_query_corpus, dev_json_multi_field_corpus):
    funcs =[ partial(CosineFIndex._tfidf_query_model_kargs) for _ in
        dev_json_multi_field_corpus.fields ]
    return TransformedCorpus(dev_query_corpus, dev_json_multi_field_corpus, funcs)

@pytest.fixture(scope = "session")
def dev_bm25_query_corpus(dev_query_corpus, dev_json_multi_field_corpus):
    funcs =[ partial(BM25FIndex._tfidf_query_model_kargs) for _ in
        dev_json_multi_field_corpus.fields ]
    return TransformedCorpus(dev_query_corpus, dev_json_multi_field_corpus, funcs)

@pytest.fixture(scope = "session")
def dev_json_multi_field_corpus(dev_text_path, dev_dictionary):
    return JsonMultiFieldCorpus(dev_text_path, fields, dictionary = dev_dictionary)

@pytest.fixture(scope = "session")
def dev_binary_json_multi_field_corpus(dev_json_multi_field_corpus):
    funcs =[ partial(JaccardFIndex._tfidf_model_kargs) for _ in
        dev_json_multi_field_corpus.fields ]
    return TransformedCorpus(dev_json_multi_field_corpus, dev_json_multi_field_corpus, funcs)

@pytest.fixture(scope = "session")
def dev_cosine_json_multi_field_corpus(dev_json_multi_field_corpus):
    funcs =[ partial(CosineFIndex._tfidf_model_kargs) for _ in
        dev_json_multi_field_corpus.fields ]
    return TransformedCorpus(dev_json_multi_field_corpus, dev_json_multi_field_corpus, funcs)

@pytest.fixture(scope = "session")
def dev_bm25_json_multi_field_corpus(dev_json_multi_field_corpus):
    funcs =[ partial(BM25FIndex._tfidf_model_kargs, slope = B) for _, B in
        zip(dev_json_multi_field_corpus.fields, Bs) ]
    return TransformedCorpus(dev_json_multi_field_corpus, dev_json_multi_field_corpus, funcs)

@pytest.fixture(scope = "session")
def dev_generate_mm_files(dev_json_multi_field_corpus):
    temp_dir = tempfile.mkdtemp()
    base_path = "{}/corpus".format(temp_dir)
    output_files = dev_json_multi_field_corpus.save_as_mm(base_path)
    yield base_path
    list(map(os.remove, output_files))

@pytest.fixture(scope = "session")
def dev_generate_binary_mm_files(dev_binary_json_multi_field_corpus):
    temp_dir = tempfile.mkdtemp()
    base_path = "{}/corpus".format(temp_dir)
    output_files = dev_binary_json_multi_field_corpus.save_as_mm(base_path)
    yield base_path
    list(map(os.remove, output_files))

@pytest.fixture(scope = "session")
def dev_generate_cosine_mm_files(dev_cosine_json_multi_field_corpus):
    temp_dir = tempfile.mkdtemp()
    base_path = "{}/corpus".format(temp_dir)
    output_files = dev_cosine_json_multi_field_corpus.save_as_mm(base_path)
    yield base_path
    list(map(os.remove, output_files))

@pytest.fixture(scope = "session")
def dev_generate_bm25_mm_files(dev_bm25_json_multi_field_corpus):
    temp_dir = tempfile.mkdtemp()
    base_path = "{}/corpus".format(temp_dir)
    output_files = dev_bm25_json_multi_field_corpus.save_as_mm(base_path)
    yield base_path
    list(map(os.remove, output_files))

@pytest.fixture(scope = "session")
def dev_mm_multi_field_corpus(dev_generate_mm_files):
    return MultiFieldCorpusABC.load_mm(dev_generate_mm_files)

@pytest.fixture(scope = "session")
def dev_binary_mm_multi_field_corpus(dev_generate_binary_mm_files):
    return MultiFieldCorpusABC.load_mm(dev_generate_binary_mm_files)

@pytest.fixture(scope = "session")
def dev_cosine_mm_multi_field_corpus(dev_generate_cosine_mm_files):
    return MultiFieldCorpusABC.load_mm(dev_generate_cosine_mm_files)

@pytest.fixture(scope = "session")
def dev_bm25_mm_multi_field_corpus(dev_generate_bm25_mm_files):
    return MultiFieldCorpusABC.load_mm(dev_generate_bm25_mm_files)

@pytest.fixture(scope = "session")
def dev_jaccard_multi_index(dev_binary_mm_multi_field_corpus):
    return JaccardFIndex(dev_binary_mm_multi_field_corpus, weights)

@pytest.fixture(scope = "session")
def dev_mapper(dev_mapping_path):
    return Mapper(read_mapping_file(dev_mapping_path))

@pytest.fixture(scope = "session")
def dev_re_index(dev_mapper):
    return ReIndex(dev_mapper.id_map, dev_mapper.match_expressions([]))

@pytest.fixture(scope = "session")
def dev_jaccard_query_response_set(dev_jaccard_multi_index,
        dev_binary_query_corpus):
    dev = dev_jaccard_multi_index.resolve_all(dev_binary_query_corpus)
    return dev

@pytest.fixture(scope = "session")
def dev_trec_files(dev_jaccard_query_response_set, dev_transition, dev_re_index):
    prefix = "test"
    with tempfile.TemporaryDirectory() as base_path:
        out_files = execute_all_models_default(dev_jaccard_query_response_set,
                dev_transition, dev_re_index, prefix, base_path)
        yield (base_path, prefix, out_files)

# Variables

fields = ['field1', 'field2']
weights = [0.75, 0.25]
Bs = [0.5, 0.5]
k = 1.7
