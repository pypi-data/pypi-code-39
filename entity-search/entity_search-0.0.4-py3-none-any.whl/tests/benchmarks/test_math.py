import pytest
import colorlog
import scipy as sp
import sparse
from entity_search.math import *

@pytest.fixture(scope = "session")
def prod_graph_dimensions():
    return (10000000, 0.00000001)

@pytest.fixture(scope = "session")
def dev_graph_dimensions():
    return (10000, 0.001)

@pytest.fixture(scope = "session")
def prod_rand_adjacency(prod_graph_dimensions):
    n, density = prod_graph_dimensions
    return sparse.random((n, n), density = density).tocsc()

@pytest.fixture(scope = "session")
def dev_rand_adjacency(dev_graph_dimensions):
    n, density = dev_graph_dimensions
    return sparse.random((n, n), density = density).tocsc()

def test_sparse_column_vector(benchmark):
    vector = np.arange(1000)
    benchmark(sparse_column_vector, vector)

@pytest.mark.parametrize("func", [ sparse_vector_to_sparse_diagonal_dia,
    sparse_vector_to_sparse_diagonal_csc])
def test_sparse_vector_to_sparse_diagonal(benchmark, func):
    vector = sparse.random((1000, 1), density = 0.01).tocsc()
    benchmark(func, vector, 1000)

def test_sum_along_rows_prod(benchmark, prod_rand_adjacency):
    benchmark(sum_along_rows, prod_rand_adjacency)

def test_sum_along_columns_prod(benchmark, prod_rand_adjacency):
    benchmark(sum_along_columns, prod_rand_adjacency)

def test_sum_along_rows_dev(benchmark, dev_rand_adjacency):
    benchmark(sum_along_rows, dev_rand_adjacency)

def test_sum_along_columns_dev(benchmark, dev_rand_adjacency):
    benchmark(sum_along_columns, dev_rand_adjacency)

def test_left_division(benchmark, dev_rand_adjacency):
    B = np.random.rand(dev_rand_adjacency.shape[0])
    benchmark(left_division, dev_rand_adjacency, B)

def test_normalise_prod(benchmark, prod_rand_adjacency):
    benchmark(normalise, prod_rand_adjacency)

def test_normalise_dev(benchmark, dev_rand_adjacency):
    benchmark(normalise, dev_rand_adjacency)

@pytest.mark.parametrize("n", [2])
@pytest.mark.parametrize("m", [10000])
@pytest.mark.parametrize("k", [2000])
def test_jaccard_norm(benchmark, n, m, k):
    rvs = lambda x: np.int32(1)
    sets1 = sparse.concatenate([
        sparse.random((k, 1), density = 0.25, data_rvs = rvs)
        for i in range(n) ], axis = 1).tocsc()
    sets2 = sparse.concatenate([
        sparse.random((1, k), density = 0.5, data_rvs = rvs)
        for i in range(m) ], axis = 0).tocsc()
    intersection = sets2 * sets1
    length_sets1 = sum_along_columns(sets1)
    length_sets2 = sum_along_rows(sets2)
    benchmark(jaccard_norm, intersection, length_sets1, length_sets2)
