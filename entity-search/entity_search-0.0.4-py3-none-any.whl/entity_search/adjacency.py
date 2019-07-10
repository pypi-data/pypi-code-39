import numpy as np
import scipy as sp
import pandas as pd
from itertools import groupby
from functools import reduce
from operator import itemgetter
import sparse
import gensim
from .math import normalise

class Tensor(gensim.utils.SaveLoad):
    """This is a tensor object
    It contains a tensor (sparse.COO matrix) and a model name
    """
    def __init__(self, sparse_coo_matrix, model):
        self.tensor = sparse_coo_matrix
        self.model = model

    def __str__(self):
        return self.model

class EqualWeight(Tensor):
    """This is a weight schema for and the list of adjacency matrices where
    each edge has equal weight.
    Args:
       adjacency: An adjacency tensor (sparse.COO).
    """
    def __init__(self, adjacency):
        super().__init__(adjacency, "eqv")

## TODO: Move part of the code to math.py
class PfitfWeight(Tensor):
    """Predicate frequency - inverse triple frequency. A weight schema similar
    to tf-idf.
    """
    def __init__(self, adjacency):
        I,_,K = adjacency.shape

        pf = self._pf(adjacency)
        new_mat = []
        for k in range(K):
            block = []
            for i in range(I):
                block.append(adjacency[i,:,k].reshape((I,1)) * pf[k*I+i] )
            new_mat.append(sparse.concatenate(block, axis = 1).T.reshape((I,I,1)))
        mat = sparse.concatenate(new_mat, axis = 2)

        itf = self._itf(adjacency)
        new_mat = []
        for k in range(K):
            new_mat.append(mat[:,:,k].reshape((I,I,1)) * itf[k])
        mat = sparse.concatenate(new_mat, axis = 2)
        super().__init__(mat, 'pfitf')

    def _itf(self, mat):
        """Inverse triple frequency (itf). It is the overall number of triples
        in the tripleSet divided by the number of triple for a given
        predicate:

        itf_p = log(#triples/#triples_p)

        Response:
            a vector containing the itfs for every predicate p
        """
        I = mat.shape[0]
        K = mat.shape[2]
        triples = mat.sum()
        triples_per_predicate = np.log(triples / np.array([
            mat[:,:,k].sum() for k in range(K)
            ]))
        return triples_per_predicate

    def _pf(self, mat):
        """Predicate frequency (pf). It is the number of triple for given node
        and certain predicate divided by the overall number of triple for the
        same node.

        pf_(p,w) = #triples_(p,w) / #triples_(p)

        In order to compute it faster, we used a vectorial approach.

        Response:
            a list of diagonal matrices, containing the score pf.
        """
        I = mat.shape[0] # num of nodes
        K = mat.shape[2] # num of predicates
        triples_per_node_predicate = np.array([ mat[i,:,k].sum()
            for i in range(I)
            for k in range(K)
            ])
        triples_per_node = np.array([np.sum(
            triples_per_node_predicate[x*K:(x+1)*K] )
            for x in range(len(triples_per_node_predicate)// K)
            ])
        ratio = np.array([triples_per_node_predicate[i*K+x]/triples_per_node[i]
            if triples_per_node[i] > 0 else 0
            for x in range(K)
            for i in range(I)
            ])
        return ratio

## TODO: Move some code to math.py
class ExclusivityWeight(Tensor):
    """Exclusivity weight schema. The weight of the edges are inversily
    propertional to the degree of rareness of the edge type.
    """
    def __init__(self, adjacency):
        I,_,K = adjacency.shape
        new_mat = []
        for k in range(K):
            new_mat.append(self.exclusivity(adjacency[:,:, k]).reshape((I,I,1)))
        mat = sparse.concatenate(new_mat, axis = 2)
        super().__init__(mat, 'excl')

    def exclusivity(self, adjacency):
        """Compute exclusivity score for an adjacency matrix of certain
        relationship type.
        Exclusivity is the reciprocal of the summation between the number of
        nodes of type p leaving node1 and the number of nodes of type p
        coming to node2, minus 1.

        Excl(n1, n2, p) = 1 / (|n1->*|(p) + |*->n2|(p) - 1 )

        To speed up this computation, we pre-compute the summation of triples
        for each type and node. Then, we compute the exclusivity for the
        entire matrix using a vectorial approach.
        Args:
            adjacency: A sparse coo matrix containing the adjecency for a
            certain relationship type.
        Response:
            A sparse coo matrix with the exclusivity score (float).
        """
        nodes1,nodes2 = adjacency.nonzero()
        # get degree
        outgoing_deg = adjacency.sum(axis = 1).todense()
        incoming_deg = adjacency.sum(axis = 0).todense()
        # compute exclusivity
        summation = outgoing_deg[nodes1] + incoming_deg[nodes2] - 1
        exclusivity = np.zeros_like(summation, dtype = 'f')
        np.divide(1, summation, out = exclusivity, where=summation!=0)
        # create new matrix
        result = sparse.COO([nodes1,nodes2], exclusivity, shape = adjacency.shape)
        return result

class Compressor(Tensor):
    """This class compress a tensor into a matrix.
    Args:
        weighting: A weighting object to compress into a matrix.
    Response:
        a matrix representation of the tensor.
    """
    def __init__(self, weighting):
        super().__init__(weighting.tensor.sum(axis = 2), str(weighting))

class Transition(Tensor):
    """This is a transition matrix
    The matrix is forced to be symetric and then a normalisation
    is computed.
    Args
        compressor: a compressed matrix.
    """
    def __init__(self, compressor):
        tran = normalise(compressor.tensor + compressor.tensor.T)
        tran = tran.T.tocsc() # Transition matrix is right stochastic
        super().__init__(tran,
                str(compressor))
