import pytest
import colorlog
from entity_search.diffusion import PureText
from entity_search.diffusion.truncate import *
from entity_search.diffusion.power_iteration import *
from .helpers import *

logger = colorlog.getLogger(__name__)

def test_pure_text(tes_transition):
    pt = PureText(tes_transition)
    assert str(pt) == "eqv_text"

@pytest.mark.skip(reason="it can take a while")
def test_katz_actual(tes_transition):
    ka = KatzActual(tes_transition, 0.5)
    assert str(ka) == "eqv_katz_actual"

def test_katz_truncate(tes_transition):
    kt = KatzTruncate(tes_transition, 2, 0.5)
    assert str(kt) == "eqv_katz_tr-2_lazy-0.5"

def test_pagerank_truncate(tes_transition):
    pt = PageRankTruncate(tes_transition, 2, 0.5)
    assert str(pt) == "eqv_prank_tr-2_lazy-0.5"

def test_heatkatz_truncate(tes_transition):
    ht = HeatKatzTruncate(tes_transition, 2, 0.5, 0.1, 1)
    assert str(ht) == "eqv_heat_tr-2_lazy-0.5_0.1_1"

def test_katz_poweriter(tes_transition):
    kp = KatzPowerIteration(tes_transition, 2, 0.5)
    assert str(kp) == "eqv_katz_pi-2_kernel-empty_lazy-0.5"

def test_pagerank_poweriter(tes_transition):
    pp = PagerankPowerIteration(tes_transition, 2, 0.5)
    assert str(pp) == "eqv_prank_pi-2_kernel-empty_lazy-0.5"

def test_p_pagerank_poweriter(tes_transition, tes_query_corpus, tes_jaccard_index):
    queries = tes_jaccard_index.resolve_all(tes_query_corpus)
    pp = PersonalisedPagerankPowerIteration(tes_transition, 2, 1.0)
    assert str(pp) == "eqv_pprank_pi-2_kernel-empty_lazy-1.0"
    r = pp.query(queries.matrix)
    assert r.shape[0] == queries.matrix.shape[0]

def test_heat_pagerank_poweriter(tes_transition):
    hp = HeatPagerankPowerIteration(tes_transition, 2, 0.5, 1.0)
    assert str(hp) == "eqv_prank_pi-2_kernel-heat-1.0_lazy-0.5"

def test_heat_p_pagerank_poweriter(tes_transition):
    hp = HeatPersonalisedPagerankPowerIteration(tes_transition, 2, 0.5, 1.0)
    assert str(hp) == "eqv_pprank_pi-2_kernel-heat-1.0_lazy-0.5"
