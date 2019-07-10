import numpy as np
import scipy as sp
from . import Diffusion
from ..math import normalise, normalise_col

##### Kernels
class Kernel(object):
    """This is a kernel for the diffusion process
    """
    def apply(self, ini_vec, t, mat_result):
        raise NotImplementedError

    def __str__(self):
        return "kernel"

class EmptyKernel(Kernel):
    def apply(self, ini_vec, t, mat_result):
        return mat_result

    def __str__(self):
        return "{}-{}".format(super().__str__(), "empty")

class HeatKernel(Kernel):
    def __init__(self, gamma):
        self.gamma = gamma
        super().__init__()

    def apply(self, ini_vec, t, mat_result):
        return (1 - self.gamma/t) * ini_vec + (self.gamma/t) * mat_result

    def __str__(self):
        return "{}-{}-{}".format(super().__str__(), "heat", self.gamma)

#### Power iteration
class PowerIteration(Diffusion):
    """This class defines the basic functionalities for a diffusion process,
    using Power Iteration algorithm (Jacobi)
    Args:
        transition: the transition matrix.
        t: number of iterations.
        globalg: whether the teleporting is global or not.
        kernel: the diffusion kernel to use
    """
    def __init__(self, transition, t, kernel = None):
        #Note that we assume the matrix is right stochastic!
        matrix = transition.tensor
        self.t = t
        self.kernel = kernel
        if self.kernel == None:
            self.kernel = EmptyKernel()
        super().__init__(matrix, str(transition))

    def mat(self, ini_vec, g):
        """
        Get an iteration over the stochastic matrix
        Args:
            ini_vec: initial vector
            g: teleporting vector
        Response:
            an updated vector
        """
        raise NotImplementedError

    def teleporting(self, ini_vec):
        """
        Get the teleporting distribution
        Args:
            ini_vec: initial vector
        Response:
            A numpy column array with the teleporting values
        """
        raise NotImplementedError

    def query(self, ini_vec):
        """Get the query result for a initial vector ini_vec.
        Args:
            ini_vec: a numpy vector with the initial values.
        Response:
            The resulting vector of the power iteration.
        """
        # We do not normalise ini_vec as it speeds up the convergance.
        g = self.teleporting(ini_vec)
        for _ in range(self.t):
            new_vec = self.kernel.apply(ini_vec, self.t, self.mat(ini_vec, g))
            ini_vec = normalise_col(new_vec)
        return ini_vec

    def __str__(self):
        pi = "pi-{}".format(self.t)
        return "{}_{}_{}".format(super().__str__(), pi, str(self.kernel))

class LazyPowerIteration(PowerIteration):
    """This class has an atenuation parameter (beta) that
    penalises longer paths
    Args:
        transition: The transition matrix.
        t: The length of the iteration process.
        beta: The atenuation parameter.
    """
    def __init__(self, transition, t, beta, **kargs):
        self.beta = beta
        super().__init__(transition, t, **kargs)
        # update matrix with beta
        self.matrix = self.matrix * beta

    def __str__(self):
        lazy="lazy-{}".format(self.beta)
        return "{}_{}".format(super().__str__(), lazy)

class KatzPowerIteration(LazyPowerIteration):
    """Computes Katz with no kernel using Power iteration approch
    """
    name = "katz"

    def mat(self, ini_vec, g):
        # matrix = beta * transition.T
        return self.matrix * ini_vec

    def teleporting(self, ini_vec):
        return None

class PagerankPowerIteration(LazyPowerIteration):
    """Computes Pagerank with no kernel using Power iteration approch
    """
    name = "prank"

    def mat(self, ini_vec, g):
        # matrix = beta * transition.T
        # g = (1-beta)*g
        return self.matrix * ini_vec + g

    def teleporting(self, ini_vec):
        # If the number of iterations is set to 1
        # the telporting probabilit will acts as a
        # constant for ini_vec, not affecting the
        # ranking itself. Thus, we can set the
        # telporting as a zero vector
        if self.t <= 1:
            return sp.sparse.dok_matrix(ini_vec.shape).tocsc()
        else:
            raise NotImplementedError

class PersonalisedPagerankPowerIteration(PagerankPowerIteration):
    """Computes Personalised Pagerank with no kernel using Power iteration approch
    Args:
        transition: The transition matrix.
        t: The length of the iteration process.
        beta: The parameter of decay.
    """
    name = "pprank"
    def __init__(self, transition, t, beta, **kargs):
        super().__init__(transition, t, beta, **kargs)

    def teleporting(self, ini_vec):
        return (1-self.beta)* normalise_col(ini_vec)

class HeatPagerankPowerIteration(PagerankPowerIteration):
    """Computes Pagerank with a heat kernel using Power iteration approach
    Args:
        transition: The transition matrix.
        t: The length of the iteration process.
        beta: The parameter of decay.
        gamma: The heat conductivity parameter
    """
    def __init__(self, transition, t, beta, gamma):
        super().__init__(transition, t, beta, kernel = HeatKernel(gamma) )

class HeatPersonalisedPagerankPowerIteration(PersonalisedPagerankPowerIteration):
    """Computes Personalised Pagerank with a heat kernel using Power iteration approach
    Args:
        transition: The transition matrix.
        t: The length of the iteration process.
        beta: The parameter of decay.
        gamma: The heat conductivity parameter
    """
    def __init__(self, transition, t, beta, gamma):
        super().__init__(transition, t, beta, kernel = HeatKernel(gamma) )
