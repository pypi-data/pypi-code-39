import pytest
import colorlog
import sparse
from entity_search.adjacency import Transition, Compressor, EqualWeight, PfitfWeight, ExclusivityWeight
from entity_search.utilities import triple_set_to_sparse_matrix
from .helpers import *


@pytest.fixture
def mini_triple_set():
    _subject = np.array([0,1,1,0,1])
    _object = np.array([1,0,1,0,1])
    _predicate = np.array([0,0,0,1,1])
    return make_triple_set(_subject, _object, _predicate)

@pytest.fixture
def mini_adjacency_matrix(mini_triple_set):
    return triple_set_to_sparse_matrix(mini_triple_set)

@pytest.fixture
def small_triple_set():
    _subject = np.array([0,1,1,3,4,5,6,7,8,9])
    _object = np.array([2,3,3,2,3,1,1,3,6,4])
    _predicate = np.array([0,1,2,0,1,2,0,1,2,0])
    return make_triple_set(_subject, _object, _predicate)

@pytest.fixture
def small_adjacency_matrix(small_triple_set):
    return triple_set_to_sparse_matrix(small_triple_set)

# Matrices

#  0 1   0 1
#0 0 1   1 0
#1 1 1   0 1

def test_equal_weight_mini(mini_adjacency_matrix):
    eq = EqualWeight(mini_adjacency_matrix)
    assert eq.tensor.shape == (2,2,2)
    assert eq.tensor.nnz == 5
    assert eq.tensor[0,1,0] == 1
    assert eq.tensor[1,0,0] == 1
    assert eq.tensor[1,1,0] == 1
    assert eq.tensor[0,0,1] == 1
    assert eq.tensor[1,1,1] == 1

def test_compressor_equal_weight_mini(mini_adjacency_matrix):
    eq = Compressor(EqualWeight(mini_adjacency_matrix))
    assert eq.tensor.shape == (2,2)
    assert eq.tensor.nnz == 4
    assert eq.tensor[0,0] == 1
    assert eq.tensor[0,1] == 1
    assert eq.tensor[1,0] == 1
    assert eq.tensor[1,1] == 2

def test_transition_equal_weight_mini(mini_adjacency_matrix):
    eq = Transition(Compressor(EqualWeight(mini_adjacency_matrix)))
    assert eq.tensor.shape == (2,2)
    assert eq.tensor.nnz == 4
    assert eq.tensor[0,0] == pytest.approx(0.5, 0.01)
    assert eq.tensor[0,1] == pytest.approx(0.333, 0.01)
    assert eq.tensor[1,0] == pytest.approx(0.5, 0.01)
    assert eq.tensor[1,1] == pytest.approx(0.666, 0.01)

def test_pfitf_weight_mini(mini_adjacency_matrix):
    pfitf = PfitfWeight(mini_adjacency_matrix)
    assert pfitf.tensor.shape == (2,2,2)
    assert pfitf.tensor.nnz == 5
    assert pfitf.tensor[0,1,0] == pytest.approx(0.255, 0.01)
    assert pfitf.tensor[1,0,0] == pytest.approx(0.340, 0.01)
    assert pfitf.tensor[1,1,0] == pytest.approx(0.340, 0.01)
    assert pfitf.tensor[0,0,1] == pytest.approx(0.458, 0.01)
    assert pfitf.tensor[1,1,1] == pytest.approx(0.305, 0.01)

def test_compressor_pfitf_weight_mini(mini_adjacency_matrix):
    pfitf = Compressor(PfitfWeight(mini_adjacency_matrix))
    assert pfitf.tensor.shape == (2,2)
    assert pfitf.tensor.nnz == 4
    assert pfitf.tensor[0,0] == pytest.approx(0.458, 0.01)
    assert pfitf.tensor[0,1] == pytest.approx(0.255, 0.01)
    assert pfitf.tensor[1,0] == pytest.approx(0.341, 0.01)
    assert pfitf.tensor[1,1] == pytest.approx(0.646, 0.01)

def test_transition_pfitf_weight_mini(mini_adjacency_matrix):
    pfitf = Transition(Compressor(PfitfWeight(mini_adjacency_matrix)))
    assert pfitf.tensor.shape == (2,2)
    assert pfitf.tensor.nnz == 4
    assert pfitf.tensor[0,0] == pytest.approx(0.605, 0.01)
    assert pfitf.tensor[0,1] == pytest.approx(0.315, 0.01)
    assert pfitf.tensor[1,0] == pytest.approx(0.394, 0.01)
    assert pfitf.tensor[1,1] == pytest.approx(0.684, 0.01)

def test_exclusivity_weight_mini(mini_adjacency_matrix):
    excl = ExclusivityWeight(mini_adjacency_matrix)
    assert excl.tensor.shape == (2,2,2)
    assert excl.tensor.nnz == 5
    assert excl.tensor[0,1,0] == pytest.approx(0.5, 0.01)
    assert excl.tensor[1,0,0] == pytest.approx(0.5, 0.01)
    assert excl.tensor[1,1,0] == pytest.approx(0.333, 0.01)
    assert excl.tensor[0,0,1] == pytest.approx(1.0, 0.01)
    assert excl.tensor[1,1,1] == pytest.approx(1.0, 0.01)

def test_compressor_exclusivity_weight_mini(mini_adjacency_matrix):
    excl = Compressor(ExclusivityWeight(mini_adjacency_matrix))
    assert excl.tensor.shape == (2,2)
    assert excl.tensor.nnz == 4
    assert excl.tensor[0,0] == pytest.approx(1.0, 0.01)
    assert excl.tensor[0,1] == pytest.approx(0.5, 0.01)
    assert excl.tensor[1,0] == pytest.approx(0.5, 0.01)
    assert excl.tensor[1,1] == pytest.approx(1.333, 0.01)

def test_transition_exclusivity_weight_mini(mini_adjacency_matrix):
    excl = Transition(Compressor(ExclusivityWeight(mini_adjacency_matrix)))
    assert excl.tensor.shape == (2,2)
    assert excl.tensor.nnz == 4
    assert excl.tensor[0,0] == pytest.approx(0.666, 0.01)
    assert excl.tensor[0,1] == pytest.approx(0.272, 0.01)
    assert excl.tensor[1,0] == pytest.approx(0.333, 0.01)
    assert excl.tensor[1,1] == pytest.approx(0.727, 0.01)

#  0 1 2 3 4 5 6 7 8 9   0 1 2 3 4 5 6 7 8 9   0 1 2 3 4 5 6 7 8 9
#0     1                                                                 1
#1                             1                     1                   2
#2                                                                       0
#3     1                                                                 1
#4                             1                                         1
#5                                               1                       1
#6   1                                                                   1
#7                             1                                         1
#8                                                         1             1
#9         1                                                             1

def test_equal_weight(small_adjacency_matrix):
    eq = Compressor(EqualWeight(small_adjacency_matrix))
    assert eq.tensor.shape == (10, 10)
    assert eq.tensor.nnz == 9
    assert eq.tensor[0,2] == 1
    assert eq.tensor[1,3] == 2
    assert eq.tensor[3,2] == 1
    assert eq.tensor[4,3] == 1
    assert eq.tensor[5,1] == 1
    assert eq.tensor[6,1] == 1
    assert eq.tensor[7,3] == 1
    assert eq.tensor[8,6] == 1
    assert eq.tensor[9,4] == 1

def test_pfitf_weight(small_adjacency_matrix):
    pfitf = Compressor(PfitfWeight(small_adjacency_matrix))
    assert pfitf.tensor.shape == (10, 10)
    assert pfitf.tensor.nnz == 9
    assert pfitf.tensor[0,2] == pytest.approx(0.916,0.01)
    assert pfitf.tensor[1,3] == pytest.approx(1.204,0.01)
    assert pfitf.tensor[3,2] == pytest.approx(0.916,0.01)
    assert pfitf.tensor[4,3] == pytest.approx(1.204,0.01)
    assert pfitf.tensor[5,1] == pytest.approx(1.204,0.01)
    assert pfitf.tensor[6,1] == pytest.approx(0.916,0.01)
    assert pfitf.tensor[7,3] == pytest.approx(1.204,0.01)
    assert pfitf.tensor[8,6] == pytest.approx(1.204,0.01)
    assert pfitf.tensor[9,4] == pytest.approx(0.916,0.01)

def test_exclusivity_weight(small_adjacency_matrix):
    excl = Compressor(ExclusivityWeight(small_adjacency_matrix))
    assert excl.tensor.shape == (10, 10)
    assert excl.tensor.nnz == 9
    assert excl.tensor[0,2] == pytest.approx(0.5,0.01)
    assert excl.tensor[1,3] == pytest.approx(1.33,0.01)
    assert excl.tensor[3,2] == pytest.approx(0.5,0.01)
    assert excl.tensor[4,3] == pytest.approx(0.333,0.01)
    assert excl.tensor[5,1] == pytest.approx(1.0,0.01)
    assert excl.tensor[6,1] == pytest.approx(1.0,0.01)
    assert excl.tensor[7,3] == pytest.approx(0.333,0.01)
    assert excl.tensor[8,6] == pytest.approx(1.0,0.01)
    assert excl.tensor[9,4] == pytest.approx(1.0,0.01)
