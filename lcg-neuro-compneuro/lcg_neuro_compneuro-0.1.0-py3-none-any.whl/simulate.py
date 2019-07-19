"""
"""

import numpy
import numpy.random


def poisson_spikes(rate, duration, size):
    r"""Generate spikes based on a constant-rate Poisson process.

    Since the number of samples is specified manually, the simulation time-step :math:`\Delta t` is determined by
    dividing the duration :math:`T` by the number of samples :math:`N`. The probability mass function for :math:`k`
    spikes in each timestep is

    .. math::

        P(k) = \frac{e^{-\lambda\Delta t} (\lambda\Delta t)^k}{k!}

    where :math:`\Delta t = T/N`, as explained above, and :math:`\lambda` is the mean firing rate (spikes per time unit)

    Parameters
    ----------
    rate: float
        Mean firing rate (spikes per second), *i.e.* :math:`\lambda`.

    duration: float
        Total duration of simulated interval, *i.e.* :math:`T`.

    size: int
        Number of samples of the simulated interval, *i.e.* :math:`N`.

    Returns
    -------
    spike_train: :class:`numpy.ndarray`
        An array that contains the number of spikes in each of the :code:`size` time-steps.
    """
    try:
        assert duration > 0
    except AssertionError:
        raise ValueError("duration must be positive")

    lam = rate * duration / size
    return numpy.random.poisson(lam=lam, size=size)
