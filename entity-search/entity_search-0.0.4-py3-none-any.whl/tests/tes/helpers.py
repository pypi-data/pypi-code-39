import pytest
import gensim
import tempfile
import os
import numpy as np
import pandas as pd
from entity_search.adjacency import EqualWeight, Compressor, Transition
from entity_search.utilities import triple_set_to_sparse_matrix, read_adjacency_file, read_mapping_file
from entity_search.multitext.corpus import *
from entity_search.multitext.indices import JaccardFIndex
from entity_search.multitext.transform import *
from entity_search.queries import ReIndex, Mapper
from entity_search.run import execute_all_models_default
from ..helpers import *

# File paths
@pytest.fixture(scope="session")
def tes_text_path(tes_dataset_path):
    return "{}/{}".format(tes_dataset_path, "toynetwork-1-filtered-text.json.bz2")

@pytest.fixture(scope="session")
def tes_qrels_path(tes_dataset_path):
    return "{}/{}".format(tes_dataset_path, "qrels.txt")

@pytest.fixture(scope="session")
def tes_queries_path(tes_dataset_path):
    return "{}/{}".format(tes_dataset_path, "queries.txt")

@pytest.fixture(scope="session")
def tes_mapping_path(tes_dataset_path):
    return "{}/{}".format(tes_dataset_path, "toynetwork-1-filtered-mapping.csv.bz2")

@pytest.fixture(scope="session")
def tes_adjacency_path(tes_dataset_path):
    return "{}/{}".format(tes_dataset_path, "toynetwork-1-filtered-adjacency.csv.bz2")

@pytest.fixture(scope="session")
def tes_groundtruth_path(tes_dataset_path):
    return "{}/{}".format(tes_dataset_path, "qrels.txt")

# Objects

@pytest.fixture(scope = "session")
def tes_transition(tes_adjacency_path):
    return Transition(Compressor(EqualWeight(read_adjacency_file(tes_adjacency_path))))

@pytest.fixture(scope = "session")
def tes_global_field(tes_text_path):
    return JsonGlobalField(tes_text_path)

@pytest.fixture(scope = "session")
def tes_single_field(tes_text_path, tes_dictionary):
    return JsonSingleField(tes_text_path, fields[0], tes_dictionary)

@pytest.fixture(scope = "session")
def tes_dictionary(tes_global_field):
    return tes_global_field.dictionary

@pytest.fixture(scope = "session")
def tes_query_corpus(tes_queries_path, tes_dictionary):
    return QueryCorpus(tes_queries_path, tes_dictionary)

@pytest.fixture(scope = "session")
def tes_binary_query_corpus(tes_query_corpus, tes_json_multi_field_corpus):
    funcs =[ partial(JaccardFIndex._tfidf_query_model_kargs) for _ in
        tes_json_multi_field_corpus.fields ]
    return TransformedCorpus(tes_query_corpus, tes_json_multi_field_corpus, funcs)

@pytest.fixture(scope = "session")
def tes_cosine_query_corpus(tes_query_corpus, tes_json_multi_field_corpus):
    funcs =[ partial(CosineFIndex._tfidf_query_model_kargs) for _ in
        tes_json_multi_field_corpus.fields ]
    return TransformedCorpus(tes_query_corpus, tes_json_multi_field_corpus, funcs)

@pytest.fixture(scope = "session")
def tes_bm25_query_corpus(tes_query_corpus, tes_json_multi_field_corpus):
    funcs =[ partial(BM25FIndex._tfidf_query_model_kargs) for _ in
        tes_json_multi_field_corpus.fields ]
    return TransformedCorpus(tes_query_corpus, tes_json_multi_field_corpus, funcs)

@pytest.fixture(scope = "session")
def tes_json_multi_field_corpus(tes_text_path, tes_dictionary):
    return JsonMultiFieldCorpus(tes_text_path, fields, dictionary = tes_dictionary)

@pytest.fixture(scope = "session")
def tes_binary_json_multi_field_corpus(tes_json_multi_field_corpus):
    funcs = [ JaccardFIndex._tfidf_model_kargs for _ in tes_json_multi_field_corpus.fields]
    return TransformedCorpus(tes_json_multi_field_corpus, tes_json_multi_field_corpus, funcs)

@pytest.fixture(scope = "session")
def tes_generate_mm_files(tes_json_multi_field_corpus):
    temp_dir = tempfile.mkdtemp()
    base_path = "{}/corpus".format(temp_dir)
    output_files = tes_json_multi_field_corpus.save_as_mm(base_path)
    yield base_path
    list(map(os.remove, output_files))

@pytest.fixture(scope = "session")
def tes_generate_binary_mm_files(tes_binary_json_multi_field_corpus):
    temp_dir = tempfile.mkdtemp()
    base_path = "{}/corpus".format(temp_dir)
    output_files = tes_binary_json_multi_field_corpus.save_as_mm(base_path)
    yield base_path
    list(map(os.remove, output_files))

@pytest.fixture(scope = "session")
def tes_mm_multi_field_corpus(tes_generate_mm_files):
    return MultiFieldCorpusABC.load_mm(tes_generate_mm_files)

@pytest.fixture(scope = "session")
def tes_binary_mm_multi_field_corpus(tes_generate_binary_mm_files):
    return MultiFieldCorpusABC.load_mm(tes_generate_binary_mm_files)

@pytest.fixture(scope = "session")
def tes_jaccard_index(tes_binary_mm_multi_field_corpus):
    return JaccardFIndex(tes_binary_mm_multi_field_corpus, weights)

@pytest.fixture(scope = "session")
def tes_mapper(tes_mapping_path):
    return Mapper(read_mapping_file(tes_mapping_path))

@pytest.fixture(scope = "session")
def tes_re_index(tes_mapper):
    return ReIndex(tes_mapper.id_map, tes_mapper.match_expressions(["<dbpedia:Category:"]))

@pytest.fixture(scope = "session")
def tes_jaccard_query_response_set(tes_jaccard_index,
        tes_binary_query_corpus):
    return tes_jaccard_index.resolve_all(tes_binary_query_corpus)

@pytest.fixture(scope = "session")
def tes_trec_files(tes_jaccard_query_response_set, tes_transition, tes_re_index):
    prefix = "test"
    with tempfile.TemporaryDirectory() as base_path:
        out_files = execute_all_models_default(tes_jaccard_query_response_set,
                tes_transition, tes_re_index, prefix, base_path)
        yield (base_path, prefix, out_files)
