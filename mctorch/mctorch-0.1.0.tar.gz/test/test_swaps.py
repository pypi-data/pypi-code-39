from mctorch.util import random_swaps

def test_random_swaps_nofixed(N=1000):
    ij = random_swaps(N)
    for i in range(N):
        assert ij[i] != i

def test_random_swaps_nobigcycles(N=1000):
    """Test that no more than 2-cycles exist"""
    ij = random_swaps(N)
    for i in range(N):
        assert ij[ij[i]] == i
