import pytest
import colorlog
from entity_search.queries import ReIndex, Mapper
from entity_search.utilities import read_mapping_file
from entity_search.diffusion import PureText
from .helpers import *

def test_mapper(tes_mapping_path):
    m = Mapper(read_mapping_file(tes_mapping_path))
    assert len(m.id_map) == 6221
    assert len(m.uri_map) == 6221
    assert m.uri_to_id("<dbpedia:100_Days_to_Heaven>") == 2
    assert m.uri_to_id("<dbpedia:Category:Writers_of_modern_Arthurian_fiction>") == 1139
    assert m.id_to_uri(2246) == "<dbpedia:Guitar>"
    assert m.id_to_uri(5126) == "<dbpedia:The_Girl_Hunters>"

def test_mapper_match(tes_mapping_path):
    m = Mapper(read_mapping_file(tes_mapping_path))
    assert m.mapping.shape == (6221, 1)
    assert m.match_expression("<dbpedia:Category:").size == 330

def test_reindex(tes_transition, tes_mapper, tes_jaccard_query_response_set):
    ri = ReIndex(tes_mapper.id_map, tes_mapper.match_expressions(["<dbpedia:Category:"]))
    pt = PureText(tes_transition)
    table = ri.ranking_for_queries(pt, tes_jaccard_query_response_set)
    assert table.shape == (393, 5)
