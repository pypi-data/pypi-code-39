import pytest
import colorlog
from entity_search.diffusion.power_iteration import *
from .helpers import *
import sparse

@pytest.mark.parametrize("t", [1, 2, 3, 4])
@pytest.mark.parametrize("diffusion, args", [(KatzPowerIteration,[]),
    (PagerankPowerIteration,[]), (PersonalisedPagerankPowerIteration,[]),
    (HeatPagerankPowerIteration, [1.0]), (HeatPersonalisedPagerankPowerIteration, [1.0]) ])
def test_katz_power_iteration(benchmark, t, diffusion, args, tes_transition):
    N = tes_transition.tensor.shape[0]
    init_vec = sparse.random((N, 1), density = 0.01).todense()
    pi = diffusion(tes_transition, t, 0.5, *args)
    benchmark(pi.query, init_vec)
