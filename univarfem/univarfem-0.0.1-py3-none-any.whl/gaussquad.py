import numpy as np


class IntervalGaussianQuadrature:
    """ Gaussian quadrature on intervals """
    def __init__(self, degree):

        self._degree = degree

    def integrate(self, f, a, b):
        """ Approximate the integral of f between a and b """

        weights = np.array([5./9, 8./9, 5./9])
        qnodes = np.array([-np.sqrt(3./5), 0, np.sqrt(3./5)])

        return .5*(b-a)*sum(weights
                            * f(.5*(b-a)*qnodes + .5*(a+b)))


class RectangleGaussianQuadrature:
    """ Gaussian quadrature on a rectangle """
    def __init__(self, degree):
        self._degree = degree

    def integrate(self, f, a1, b1, a2, b2):

        qnodes = np.array([[-1., -1.],
                           [1., -1.],
                           [-1.,  1.],
                           [1.,  1.]])/np.sqrt(3.)

        weights = np.ones(4)

        return .25*(b1-a1)*(b2-a2)*np.sum(
            weights*f(.5*(b1-a1)*qnodes[:, 0] + .5*(a1+b1),
                      .5*(b2-a2)*qnodes[:, 1] + .5*(a2+b2)))
