"""This module contains convenience wrapper classes around the functions in the :mod:`compneuro.kernels` module that
allow to easily create and pass kernel factories to functions that accept abstract kernel types, like
:func:`compneuro.signal.firing_rate`. This way, it is possible to specify a kernel type without actually instantiating
the kernel and let the consuming function do this by specifying a concrete firing rate (which in turn was probably
directly passed to the consuming function).

.. todo::
    Create a decorator for abstracting this factory class declaration process, which will simplify sorting and code.
    This decorator may work by automatically creating proper submodules and classes for wrapped functions in
    :mod:`compneuro.kernels`.
"""

import compneuro.kernels


class Gaussian:
    """Kernel factories that abstract the sampling rate from :func:`compneuro.kernels.gaussian`.
    """

    def __init__(self, sigma, mu=0.0, devs=2):
        self.sigma = sigma
        self.mu = mu
        self.devs = devs

    def __call__(self, rate):
        return compneuro.kernels.gaussian(
            sigma=self.sigma, mu=self.mu, rate=rate, devs=self.devs
        )
