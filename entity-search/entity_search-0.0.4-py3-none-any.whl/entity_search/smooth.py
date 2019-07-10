import numpy as np
import scipy as sp
from .multitext.indices import QueryResponseSet

class Smooth(object):
    def __init__(self, alpha):
        self.alpha = alpha

    def to_smooth(self, query_response_set):
        mat = query_response_set.matrix
        if sp.sparse.isspmatrix(mat):
            mat = mat.power(self.alpha)
        elif isinstance(mat, np.ndarray):
            mat = np.power(mat, self.alpha)
        else:
            raise RuntimeError('Format not found')
        return QueryResponseSet(mat, query_response_set.query_names)
