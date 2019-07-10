import pytest
import colorlog
from entity_search.diffusion import PureText
from entity_search.diffusion.power_iteration import *
from entity_search.multitext.similarities import JaccardSimilarity
from entity_search.multitext.indices import JaccardFIndex
from entity_search.queries import ReIndex
from .helpers import *

logger = colorlog.getLogger(__name__)

def test_pure_text(dev_transition, dev_jaccard_query_response_set, dev_mapper):
    ri = ReIndex(dev_mapper.id_map, dev_mapper.match_expressions([]))
    rank = ri.ranking_for_queries(PureText(dev_transition), dev_jaccard_query_response_set)
    assert rank.iloc[0].id == 1
    assert rank.iloc[0].score == pytest.approx(0.6250,.001)
    assert rank.iloc[0].entity == '<dbpedia:BBB>'
    assert rank.iloc[1].id == 0
    assert rank.iloc[1].score == pytest.approx(0.2750,.001)
    assert rank.iloc[1].entity == '<dbpedia:AAA>'
    assert rank.iloc[2].id == 4
    assert rank.iloc[2].score == pytest.approx(1.0000,.001)
    assert rank.iloc[2].entity == '<dbpedia:EEE>'
    assert rank.iloc[3].id == 3
    assert rank.iloc[3].score == pytest.approx(0.5000,.001)
    assert rank.iloc[3].entity == '<dbpedia:DDD>'
    assert rank.iloc[4].id == 5
    assert rank.iloc[4].score == pytest.approx(0.3750,.001)
    assert rank.iloc[4].entity == '<dbpedia:FFF>'

def test_katz_power_iteration(dev_transition, dev_jaccard_query_response_set, dev_mapper):
    ri = ReIndex(dev_mapper.id_map, dev_mapper.match_expressions([]))
    rank = ri.ranking_for_queries(KatzPowerIteration(dev_transition, 1, 0.5),
            dev_jaccard_query_response_set)

def test_prank_power_iteration(dev_transition, dev_jaccard_query_response_set, dev_mapper):
    ri = ReIndex(dev_mapper.id_map, dev_mapper.match_expressions([]))
    rank = ri.ranking_for_queries(PagerankPowerIteration(dev_transition, 1, 0.5),
            dev_jaccard_query_response_set)

def test_pprank_power_iteration(dev_transition, dev_jaccard_query_response_set, dev_mapper):
    ri = ReIndex(dev_mapper.id_map, dev_mapper.match_expressions([]))
    rank = ri.ranking_for_queries(PersonalisedPagerankPowerIteration(dev_transition, 1, 0.5),
            dev_jaccard_query_response_set)
