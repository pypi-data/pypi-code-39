import pytest
import colorlog
import sparse
import numpy as np
import scipy as sp
from entity_search.math import *
from entity_search.utilities import triple_set_to_sparse_matrix
from .helpers import *
from .test_adjacency import small_triple_set

@pytest.mark.parametrize("n", [5, 100, 500])
def test_empty_sparse_vector(n):
    v = empty_sparse_vector(n)
    assert v.shape == (n, 1)
    assert sp.sparse.isspmatrix_csc(v)

@pytest.mark.parametrize("n", [5, 100, 500])
def test_empty_sparse_vector_dok(n):
    v = empty_sparse_vector_dok(n)
    assert v.shape == (n, 1)
    assert sp.sparse.isspmatrix_dok(v)

@pytest.mark.parametrize("n", [5, 100, 500])
def test_sparse_column_vector(n):
    v = np.random.rand(n)
    v = sparse_column_vector(v)
    assert v.shape == (n, 1)
    assert sp.sparse.isspmatrix_coo(v)

def test_sum_along_rows():
    mat = sp.sparse.csr_matrix(np.arange(10).reshape(5,2))
    s = sum_along_rows(mat)
    assert s[0] == 1
    assert s[1] == 5
    assert s[2] == 9
    assert s[3] == 13
    assert s[4] == 17

def test_sum_along_columns():
    mat = sp.sparse.csc_matrix(np.arange(10).reshape(5,2))
    s = sum_along_columns(mat)
    assert s[0] == 20
    assert s[1] == 25

@pytest.mark.parametrize("n", [100, 200])
def test_left_division(n):
    A = sp.sparse.rand(n, n, density = 0.1, format = 'csc')
    b = np.random.rand(n)
    D = left_division(A, b)
    assert D.shape == A.shape
    assert D.nnz == A.nnz
    AD = A.toarray()
    DD = D.toarray()
    m, n = A.shape
    for i in range(m):
        for j in range(n):
            assert AD[i, j] * (1/b[i]) == pytest.approx(DD[i,j], .001)

@pytest.mark.parametrize("n", [100, 200])
def test_right_division(n):
    A = sp.sparse.rand(n, n, density = 0.1, format = 'csc')
    b = np.random.rand(n)
    D = right_division(A, b)
    assert D.shape == A.shape
    assert D.nnz == A.nnz
    AD = A.toarray()
    DD = D.toarray()
    m, n = A.shape
    for i in range(m):
        for j in range(n):
            assert AD[i, j] * (1/b[j]) == pytest.approx(DD[i,j], .001)

@pytest.mark.parametrize("n", [ 100, 200])
def test_normalise_by_sparse_multiplication(n):
    A = sp.sparse.rand(n, n, density = 0.1, format = 'csc')
    N = normalise(A)
    assert N.shape == A.shape
    assert N.nnz == A.nnz
    s = np.round( N.toarray().sum(axis = 1), 2)
    assert (s <= 1).all()
    assert (s >= 0).all()
    assert not (np.logical_and( s < 1, s > 0)).all()
    assert (A.toarray().sum( axis =1)[s == 1] > 0).all()

@pytest.mark.parametrize("n", [100, 200])
def test_normalise_col(n):
    A = sp.sparse.rand(n, n, density = 0.1, format = 'csc')
    N = normalise_col(A)
    assert N.shape == A.shape
    assert N.nnz == A.nnz
    s = np.round( N.toarray().sum(axis = 0), 2)
    assert (s <= 1).all()
    assert (s >= 0).all()
    assert not (np.logical_and( s < 1,  s > 0)).all()
    assert (A.toarray().sum( axis = 0)[s == 1] > 0).all()

@pytest.mark.parametrize("n", [ 20, 50])
@pytest.mark.parametrize("func", [ sparse_vector_to_sparse_diagonal_dia,
    sparse_vector_to_sparse_diagonal_csc])
def test_sparse_vector_to_sparse_diagonal(n, func):
    v = sparse.random((n, 1), density = 0.1).tocsc()
    d = func(v, n).tocsc()
    assert d.shape == (n, n)
    assert d.nnz == v.nnz
    assert d.data[0] == v.data[0]
    assert d.data[len(v.data)-1] == v.data[len(v.data)-1]

def test_count_by():
    a = np.arange(0,10)
    b = np.arange(5,10)
    c = np.concatenate((a, b))
    count = count_by(c)
    np.testing.assert_array_equal(count['f0'], np.array([0,1,2,3,4,5,6,7,8,9]))
    np.testing.assert_array_equal(count['f1'], np.array([1,1,1,1,1,2,2,2,2,2]))

@pytest.mark.parametrize("n", [ 20, 50])
def test_sparse_eye(n):
    s = sparse_eye(n)
    assert s.shape == (n, n)
    assert s.nnz == n
    assert (s.data == 1).all()

@pytest.mark.parametrize("n", [ 20, 50])
def test_sparse_one(n):
    s = sparse_one(n)
    assert s.shape == (n, 1)
    assert s.nnz == n
    assert (s.data == 1).all()

@pytest.mark.parametrize("n", [ 20, 50])
def test_sparse_zero(n):
    s = sparse_zero(n)
    assert s.shape == (n, n)
    assert s.nnz == 0

def test_triple_set_to_sparse_matrix(small_triple_set):
    matrix = triple_set_to_sparse_matrix(small_triple_set)
    assert matrix.shape == (10, 10, 3)
    assert matrix.nnz == 10

@pytest.mark.parametrize("n", [2])
@pytest.mark.parametrize("m", [4])
@pytest.mark.parametrize("k", [10])
def test_jaccard_norm(n, m, k):
    rvs = lambda x: np.int8(1)
    sets1 = sparse.concatenate([
        sparse.random((k, 1), density = 0.25, data_rvs = rvs)
        for i in range(n) ], axis = 1).tocsc()
    sets2 = sparse.concatenate([
        sparse.random((1, k), density = 0.5, data_rvs = rvs)
        for i in range(m) ], axis = 0).tocsc()
    intersection = sets2 * sets1
    length_sets1 = sum_along_columns(sets1)
    length_sets2 = sum_along_rows(sets2)
    norm_intersection = jaccard_norm(intersection, length_sets1, length_sets2)

@pytest.mark.parametrize("m", [100, 1000])
@pytest.mark.parametrize("n", [50, 500])
def test_isin_inv(n, m):
    array1 = np.random.choice(m, n)
    array2 = np.sort(np.random.choice(m, int(n/10), replace = False))
    out = isin(array1, set(array2))
    out2 = np.isin(array1, array2)
    assert (out == out2).all()

@pytest.mark.parametrize("m", [100, 1000])
@pytest.mark.parametrize("n", [20, 50])
def test_argsort_sparse_matrix(m, n):
    max_items = 5
    matrix = sp.sparse.random(m, n, 0.1).tocsc()
    out = argsort_sparse_matrix(matrix, max_items)
    assert out.shape == (max_items, n)
    for i in range(n):
        sort = np.argsort(matrix.data[matrix.indptr[i]:matrix.indptr[i+1]])[::-1]
        if len(sort) > max_items:
            items = max_items
        else:
            items = len(sort)
        assert (out[:items,i] == sort[:items]).all()

