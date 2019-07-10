import pytest
import colorlog
import json
from entity_search.multitext.corpus import *
from .helpers import *

logger = colorlog.getLogger(__name__)

def test_global_field_json_corpus(dev_text_path):
    gfjc = JsonGlobalField(dev_text_path)
    docs = [ doc for doc in gfjc]
    assert docs[0] == [(0, 2), (1, 2), (2, 1), (3, 1), (4, 1)]
    assert docs[1] == [(1, 2), (2, 1)]
    assert docs[2] == [(2, 1), (3, 2)]
    assert docs[3] == [(3, 1), (4, 2)]
    assert docs[4] == [(2, 1), (4, 2)]
    assert docs[5] == [(4, 1)]

def test_field0_json_corpus(dev_text_path):
    sfjc = JsonSingleField(dev_text_path, fields[0])
    docs = [ doc for doc in sfjc ]
    assert docs[0] == [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)]
    assert docs[1] == [(1, 1), (2, 1)]
    assert docs[2] == [(2, 1), (3, 1)]
    assert docs[3] == [(3, 1), (4, 1)]
    assert docs[4] == [(2, 1), (4, 1)]
    assert docs[5] == [(4, 1)]

def test_field1_json_corpus(dev_text_path):
    sfjc = JsonSingleField(dev_text_path, fields[1])
    docs = [ doc for doc in sfjc ]
    assert docs[0] == [(0, 1), (1, 1)]
    assert docs[1] == [(1, 1)]
    assert docs[2] == [(2, 1)]
    assert docs[3] == [(3, 1)]
    assert docs[4] == [(3, 1)]
    assert docs[5] == []

def test_single_field_mm_corpus(dev_generate_mm_files, dev_dictionary):
    base_path = dev_generate_mm_files
    field_name = fields[0]
    field_file = "{}.{}.mm".format(base_path, field_name)
    sfmc = MmSingleField(field_file, field_name, dev_dictionary)
    docs = [ doc for doc in sfmc ]
    assert docs[0] == [(0, 1.0), (1, 1.0), (2, 1.0), (3, 1.0), (4, 1.0)]
    assert docs[1] == [(1, 1.0), (2, 1.0)]
    assert docs[2] == [(2, 1.0), (3, 1.0)]
    assert docs[3] == [(3, 1.0), (4, 1.0)]
    assert docs[4] == [(2, 1.0), (4, 1.0)]
    assert docs[5] == [(4, 1.0)]

def test_multi_field_json_corpus(dev_text_path):
    mfjc = JsonMultiFieldCorpus(dev_text_path, fields)
    field0 = [ doc for doc in mfjc.fields[0] ]
    assert field0[0] == [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)]
    assert field0[1] == [(1, 1), (2, 1)]
    assert field0[2] == [(2, 1), (3, 1)]
    assert field0[3] == [(3, 1), (4, 1)]
    assert field0[4] == [(2, 1), (4, 1)]
    assert field0[5] == [(4, 1)]
    field1 = [ doc for doc in mfjc.fields[1] ]
    assert field1[0] == [(0, 1), (1, 1)]
    assert field1[1] == [(1, 1)]
    assert field1[2] == [(3, 1)]
    assert field1[3] == [(4, 1)]
    assert field1[4] == [(4, 1)]
    assert field1[5] == []

def test_multi_field_mm_corpus(dev_generate_mm_files):
    base_path = dev_generate_mm_files
    field_files = ["{}.{}.mm".format(base_path, field_name)
            for field_name in fields ]
    dictionary_file = "{}.dict".format(base_path)
    mfmc = MmMultiFieldCorpus(field_files, fields, dictionary_file)
    field0 = [doc for doc in mfmc.fields[0]]
    assert field0[0] == [(0, 1.0), (1, 1.0), (2, 1.0), (3, 1.0), (4, 1.0)]
    assert field0[1] == [(1, 1.0), (2, 1.0)]
    assert field0[2] == [(2, 1.0), (3, 1.0)]
    assert field0[3] == [(3, 1.0), (4, 1.0)]
    assert field0[4] == [(2, 1.0), (4, 1.0)]
    assert field0[5] == [(4, 1.0)]
    field1 = [doc for doc in mfmc.fields[1]]
    assert field1[0] == [(0, 1.0), (1, 1.0)]
    assert field1[1] == [(1, 1.0)]
    assert field1[2] == [(3, 1.0)]
    assert field1[3] == [(4, 1.0)]
    assert field1[4] == [(4, 1.0)]
    assert field1[5] == []

def test_query_corpus(dev_queries_path, dev_dictionary):
    qc = QueryCorpus(dev_queries_path, dev_dictionary)
    queries = [ query for query in qc.fields[0]]
    assert len(queries) == 2
    assert queries[0] == [(1, 1)]
    assert queries[1] == [(2, 1), (4, 1)]
    ids = [_id for _id in qc.ids]
    assert len(ids) == 2
    assert ids[0] == "SemSearch_ES-1"
    assert ids[1] == "SemSearch_LS-2"

def test_instant_query_corpus(dev_queries_path, dev_dictionary):
    json_queries_list = []
    with open(dev_queries_path, 'r') as f:
        for line in f.readlines():
            text = line.strip().split('\t')
            query = {'keywords':text[1], 'id':text[0]}
            json_queries_list.append(query)
    json_queries_text = "\n".join([json.dumps(query) for query in json_queries_list])

    iqc = InstantQueryCorpus(json_queries_text, dev_dictionary)
    queries = [ query for query in iqc.fields[0]]
    assert len(queries) == 2
    assert queries[0] == [(1, 1)]
    assert queries[1] == [(2, 1), (4, 1)]
    ids = [_id for _id in iqc.ids]
    assert len(ids) == 2
    assert ids[0] == "SemSearch_ES-1"
    assert ids[1] == "SemSearch_LS-2"
