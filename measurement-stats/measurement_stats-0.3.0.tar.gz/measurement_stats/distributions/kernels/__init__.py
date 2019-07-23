import typing

import numpy as np

import measurement_stats as mstats
from measurement_stats.distributions.kernels import gaussians


class Kernel(typing.NamedTuple):
    """Data structure for Kernel objects."""

    single: typing.Callable[[float, 'mstats.ValueUncertainty', float], float]
    many: typing.Callable[[float, np.array, np.array], np.array]


GAUSSIAN_KERNEL = Kernel(
    single=gaussians.gaussian,
    many=gaussians.gaussian_many
)


def uncertainty_estimate(values):
    """
    Creates an estimate for the uncertainty to apply to each value base
    on the separation of the entries that make up the distribution. This is
    used in cases where no uncertainty was described in the measurements,
    but the measurement population is fairly large, so that the
    quantization of the measurements themselves indicate the uncertainty
    implicitly.

    :param values: An iterable containing entries for the distribution
    :type: iterable

    :return: The uniform uncertainty value to apply to all of the measurements
        within the distribution
    :rtype: float
    """

    test = list(values) + []
    test.sort()

    deltas = []
    for i in range(len(test) - 1):
        deltas.append(abs(test[i] - test[i + 1]))

    return max(0.00001, 0.5 * float(np.median(deltas)))
