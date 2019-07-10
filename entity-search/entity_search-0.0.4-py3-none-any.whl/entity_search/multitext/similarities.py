import gensim
import numpy as np
import scipy as sp
from ..interfaces import Similarity
from ..math import *

class JaccardSimilarity(Similarity):
    """ Compute Jaccard similarity
    """
    def __init__(self, corpus, num_features=None, num_terms=None,
                 num_docs=None, num_nnz=None, num_best=None, chunksize=500,
                 dtype=np.int32, maintain_sparsity=False):
        super().__init__(corpus, num_features, num_terms, num_docs, num_nnz,
                num_best, chunksize, dtype, maintain_sparsity)
        # Create sum
        self.sum = sum_along_rows(self.index)

    def get_similarities(self, query):
        """ Given a query compute the jaccard similarity.
        We prefer the generalisation proposed by Tanimoto, i.e.
        jacc(u,v) = u*v / (||u|| + ||v|| - u*v)
        Args:
            query: A query
        Response:
            A sparse vector containing the similarities
        """
        # Jaccard(M, q) = M*q / sum(M) + sum(q) - M*q
        # compute dot product against every other document in the collection
        dot_index_query = self.index * query.tocsc()  # N x T * T x C = N x C
        # normalisation using
        sum_query = sum_along_columns(query)
        # To avoid wasting time on creating a dense representation
        # we opted for using the internal components of the sparse matrix.
        # In this way, we can manipulate the content with a minimal impact on
        # the speed.
        return jaccard_norm(dot_index_query, sum_query, self.sum)

class CosineSimilarity(Similarity):
    """ Compute Jaccard similarity
    """
    def get_similarities(self, query):
        """ Given a query compute similarity.
        We use the dot product.
        Args:
            query: A sparse vector
        Response:
            A sparse vector containing the similarities
        """
        # both, index and query, are normalised thus there is no need
        # to do anything else.
        return self.index * query.tocsc()  # N x T * T x C = N x C
