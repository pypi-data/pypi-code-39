from ..adjacency import *
from ..math import sparse_eye
import scipy
import scipy.sparse
from scipy.sparse import linalg

class Diffusion(object):
    """This class defines the basic functionalities for a diffusion process,
    including identity matrix and query.
    Args:
        transition: the transition matrix.
    """
    name = 'diff'

    def __init__(self, matrix, scheme_name):
        assert scipy.sparse.isspmatrix_csc(matrix)
        self.matrix = matrix # matrix should CSC and right stochastic
        self.weighting_scheme = scheme_name

    def query(self, ini_vec):
        """Query the diffused matrix using ini_vec.
        Args:
            ini_vec: Initial vector.
        Response:
            A query output vector.
        """
        raise NotImplementedError

    def __str__(self):
        return "{}_{}".format(self.weighting_scheme, self.name)

#### PureText
class PureText(Diffusion):
    name = "text"

    def __init__(self, transition):
        super().__init__(transition.tensor, str(transition))

    def query(self, ini_vec):
        return ini_vec

# Actual methods
class Actual(Diffusion):
    """This mehtods produce the actual result of the relatedness by computing
    the inverse of the diffusion matrix. These methods are very expensive.
    Args:
        D: diffusion matrix
    """
    def __str__(self):
        return "{}_{}".format(super().__str__(), "actual")

class KatzActual(Diffusion):
    """This class produces the actual Katz relatedness, using the inverse of
    the matrix. Note that this method is very expensive.
    Args:
        transition: The transition matrix
        beta: The decay parameter
    """
    name = "katz"
    def __init__(self, transition, beta):
        T = transition.tensor
        n = T.shape[0]
        K = linalg.inv(sparse_eye(n) - beta*T)
        super().__init__(K+K.T, str(transition))
