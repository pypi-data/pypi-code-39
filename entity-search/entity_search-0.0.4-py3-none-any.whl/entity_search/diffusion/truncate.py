from . import *
from ..math import sparse_eye

# Truncate
class Truncate(Diffusion):
    """This class truncate the diffusion up to certain number of iterations
    """
    def __init__(self, transition, max_t):
        self.t = max_t
        T = transition.tensor
        n = T.shape[0]
        K = sparse_eye(n)
        Ac = sparse_eye(n)
        for i in range(0, self.t):
            Ac = Ac * self.markov_matrix(T)
            K = K + Ac
        super().__init__(K+K.T, str(transition))

    def markov_matrix(self, T):
        raise NotImplementedError

    def query(self, ini_vec):
        return np.dot(self.K, ini_vec)

    def __str__(self):
        truncate = "{}-{}".format("tr", self.t)
        return "{}_{}".format(super().__str__(), truncate)

class LazyTruncate(Truncate):
    """This class produces the accumulation of Katz value. Once initialised,
    it expands the progression until max_t, without accumulating the values.
    Only when the method acc is called, the accumulation is produced, using
    beta as the drop parameter.
    Args:
        T: The transition matrix.
        beta: The parameter of decay.
        max_t: The length of the progression.
    """
    def __init__(self, transition, max_t, beta):
        self.beta = beta
        super().__init__(transition, max_t)

    def __str__(self):
        lazy = "{}-{}".format("lazy", self.beta)
        return "{}_{}".format(super().__str__(), lazy)

class KatzTruncate(LazyTruncate):
    name = "katz"
    def markov_matrix(self, T):
        return self.beta*T

class PageRankTruncate(LazyTruncate):
    name = "prank"
    def markov_matrix(self, T):
        return self.beta*T + (1-self.beta) * sparse_eye(T.shape[0])

class HeatLazyTruncate(LazyTruncate):
    def __init__(self, transition, max_t, beta, heat_coef, n):
        self.n = n
        self.heat_coef = heat_coef
        self.Acc = None
        super().__init__(transition, max_t, beta)

    def __str__(self):
        return "{}_{}_{}".format(super().__str__(), self.heat_coef, self.n)

class HeatKatzTruncate(HeatLazyTruncate):
    name = "heat"
    def markov_matrix(self, T):
        if self.Acc == None:
            R = self.beta*T
            size = T.shape[0]
            Acc = sparse_eye(size)
            for i in range(self.n):
                Acc = Acc *( sparse_eye(size) + (self.heat_coef/self.n)*R)
            self.Acc = Acc
        return self.Acc
