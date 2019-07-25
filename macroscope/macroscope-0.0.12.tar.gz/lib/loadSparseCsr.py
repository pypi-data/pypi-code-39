# External libraries
from numpy import load

# Standard library
from scipy import sparse


def load_sparse_csr(filename):
    loader = load(filename)
    return sparse.csr_matrix((loader['data'], loader['indices'], loader['indptr']), shape=loader['shape'])
