#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""Benchmark for Numpy

Credit:

__author__ = Markus Beukelmann : email@markus-beuckelmann.de

The logic was adapted from his Github gist.
"""

from __future__ import print_function

import numpy as np

# Let's take the randomness out of random numbers (for reproducibility)
np.random.seed(0)

size = 4096
A, B = np.random.random((size, size)), np.random.random((size, size))
C, D = np.random.random((size * 128,)), np.random.random((size * 128,))
E = np.random.random((int(size / 2), int(size / 4)))
F = np.random.random((int(size / 2), int(size / 2)))
F = np.dot(F, F.T)
G = np.random.random((int(size / 2), int(size / 2)))

# Matrix multiplication
def matrix_multiplication():
    N = 20
    for i in range(N):
        np.dot(A, B)

# Vector multiplication
def vector_multiplication():
    N = 5000
    for i in range(N):
        np.dot(C, D)

# Singular Value Decomposition (SVD)
def svd():
    N = 3
    for i in range(N):
        np.linalg.svd(E, full_matrices = False)

# Cholesky Decomposition
def cholesky_decomposition()
    N = 3
    for i in range(N):
        np.linalg.cholesky(F)

# Eigendecomposition
def eigen_decomposition():
    for i in range(N):
        np.linalg.eig(G)
    np.__config__.show()

def main():
    matrix_multiplication()
    vector_multiplication()
    svd()
    cholesky_decomposition()
    eigen_decomposition()

if __name__ == "__main__":
    c = main()