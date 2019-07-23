import math
import numpy as np

import measurement_stats as mstats


def gaussian(
        x: float,
        measurement: 'mstats.ValueUncertainty',
        max_sigma: float = 10.0
) -> float:
    """
    A Gaussian kernel function that returns a probability distributions value at
    the given x position where the Gaussian is defined by the center (mean)
    and width (standard deviation)

    :param x:
        Position where the kernel should be evaluated to return the
        probability distributions value
    :param measurement:
        A ValueUncertainty instance that is used to define the parameters
        for the kernel
    :param max_sigma:
        The maximum amount of sigmas from the measurement value
        where the kernel will calculate the probability distributions. Any
        values outside of this threshold will just return a value of 0.
    :return:
        The probability for the measurement at the given x position
    """
    center = measurement.value
    width = measurement.uncertainty
    width = max(width, 1e-6)

    if x <= (center - max_sigma * width) or x >= (center + max_sigma * width):
        # Don't calculate values outside a "reasonable" 10 sigma range
        return 0.0

    coefficient = 1 / math.sqrt(2.0 * math.pi * width * width)
    exponent = -0.5 * ((float(x) - center) ** 2) / (width * width)

    return coefficient * math.exp(exponent)


def gaussian_many(
        x: float,
        values: np.array,
        uncertainties: np.array
) -> np.array:
    """
    A Gaussian kernel function that returns a probability distributions value at
    the given x position where the Gaussian is defined by the center (mean)
    and width (standard deviation)

    :param x:
    :param values:
    :param uncertainties:
    :return:
    """
    center = np.array(values)
    width = np.maximum(np.array(uncertainties), 1e-6)
    coefficient = 1 / np.sqrt(2.0 * math.pi * width * width)
    exponent = -0.5 * ((float(x) - center) ** 2) / (width * width)
    return coefficient * np.exp(exponent)
