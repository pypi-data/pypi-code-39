import typing

import numpy as np

import measurement_stats as mstats
from measurement_stats import errors
from measurement_stats import value
from measurement_stats.value import ValueUncertainty
from measurement_stats.distributions import kernels


def create(
        measurements: 'mstats.ArrayType',
        uncertainties: typing.Optional['mstats.ArrayType'] = None,
        kernel: kernels.Kernel = None
):
    """
    Creates a distribution according to the specified arguments.

    If the measurements argument is an iterable of ValueUncertainty
    instances, they are used directly to create the distribution and any
    value for the uncertainties argument is ignored.

    If the measurements argument is an iterable of numeric types then
    they are converted into ValueUncertainties using the uncertainties
    argument.

    :param kernel: (optional) A function with the signature
        kernel(x, measurement) that returns the probability for the given
        measurement at the position value x. If no kernel is specified, the
        default Gaussian kernel will be used

    :param measurements: An iterable containing each of the measurements for
        the distribution. The iterable must be a homogeneous collection of
        either ValueUncertainty instances or a numeric type.

    :param uncertainties: (optional) If no uncertainties are specified, then
        an uncertainty is estimated based on the spacing between measurements.
        If uncertainties is a single numeric value, then that value is applied
        equally to all measurements. Otherwise, uncertainties should be an
        iterable with the same length as the measurements argument and contain
        numeric values of uncertainty for each measurement accordingly. This
        argument is ignored if the measurements are already ValueUncertainties.

    :return: A Distribution instance created based on the specified arguments
    :rtype: Distribution
    """

    if measurements is None or len(measurements) == 0:
        return None

    measurements = list(measurements) + []

    if hasattr(measurements[0], 'raw'):
        # Already an iterable of ValueUncertainty instances
        return Distribution(kernel=kernel, measurements=measurements)

    if uncertainties is None:
        # If there is no uncertainty estimate one based on the spacing of the
        # points within the distribution and apply that to all of the
        # measurements
        unc = kernels.uncertainty_estimate(measurements)
        return Distribution(
            kernel=kernel,
            measurements=[ValueUncertainty(v, unc) for v in measurements]
        )

    try:
        if len(measurements) != len(uncertainties):
            raise ValueError(errors.message(
                """
                The measurements (length {}) and uncertainties
                (length {}) arguments be equal length iterables
                """,
                len(measurements),
                len(uncertainties)
            ))

        zipper = zip(measurements, uncertainties)
        return Distribution(
            kernel=kernel,
            measurements=[ValueUncertainty(v, u) for v, u in zipper]
        )
    except TypeError:
        # If the uncertainties are not a list then this will be raise and
        # we assume that uncertainties is just a number
        pass

    return Distribution(
        kernel=kernel,
        measurements=[ValueUncertainty(v, uncertainties) for v in measurements]
    )


class Distribution(object):
    """
    Data structure representing a probability distributions distribution
    for a given set of measurements and a kernel function that defines
    how the probability for each measurement is distributed along the
    measurement (i.e. x) axis.

    Each measurement entry is assumed to account for a single measurement,
    so that it accounts for an equal amount of probability within the
    distribution.

    A measurement is a ValueUncertainty instance, which resolves using the
    kernel function, to its own probability distribution along the
    measurement axis (i.e. the x axis).
    """

    def __init__(
            self,
            measurements: typing.List['mstats.ValueUncertainty'] = None,
            kernel: kernels.Kernel = None
    ):
        self.kernel = kernel if kernel else kernels.GAUSSIAN_KERNEL
        self.measurements = measurements if measurements is not None else []

        values, uncertainties = zip(*[
            (m.value, m.uncertainty)
            for m in self.measurements
        ])
        self.values = np.array(values)
        self.uncertainties = np.array(uncertainties)

    def density_at(self, x: float) -> float:
        """
        Returns the density of the distribution at the given position
        on the measurement axis (x).

        :param x:
            The position along the measurement axis where the density
            will be calculated.

        :return:
            The density at the specified position on the measurement axis.
        """
        return float(np.sum(self.kernel.many(
            x,
            self.values,
            self.uncertainties
        )))

    def densities_at(
            self,
            x_values: 'mstats.ArrayType'
    ) -> typing.List[float]:
        """
        The densities for the distribution at the given locations on
        the measurement (x) axis.

        :param x_values:
            An iterable containing the values where the
            probability of the distribution should be calculated

        :return:
            A list containing the normalized probabilities at each of the
            specified position values (floats)
        """
        return [self.density_at(x) for x in x_values]

    def heighted_density_at(
            self,
            x: 'mstats.ArrayType',
            measurement_heights: 'mstats.ArrayType'
    ) -> float:
        """..."""
        return float(np.sum(
            self.kernel.many(x, self.values, self.uncertainties)
            * np.array(measurement_heights)
        ))

    def heighted_densities_at(
            self,
            x_values: typing.List[float],
            measurement_heights: 'mstats.ArrayType'
    ) -> typing.List[float]:
        return [
            self.heighted_density_at(x, measurement_heights)
            for x in x_values
        ]

    def probability_at(self, x: float) -> float:
        """
        Returns the probability of the distribution at the given position
        on the measurement axis (x)

        :param x:
            The position along the measurement axis where the probability
            will be calculated.

        :return:
            The probability (normalized to a maximum of 1.0) at the
            specified position on the measurement axis
        """
        return self.density_at(x) / len(self.measurements)

    def probabilities_at(
            self,
            x_values: 'mstats.ArrayType'
    ) -> typing.List[float]:
        """
        The probabilities for the distribution at the given locations on
        the measurement (x) axis.

        :param x_values:
            An iterable containing the values where the
            probability of the distribution should be calculated

        :return:
            A list containing the normalized probabilities at each of the
            specified position values (floats)
        """
        return list(
            np.array(self.densities_at(x_values))
            / len(self.measurements)
        )

    def heighted_probability_at(
            self,
            x: 'mstats.ArrayType',
            measurement_heights: 'mstats.ArrayType'
    ) -> float:
        """..."""
        return float(np.sum(
            np.array(self.heighted_density_at(x, measurement_heights))
            / np.sum(np.array(measurement_heights))
        ))

    def heighted_probabilities_at(
            self,
            x_values: 'mstats.ArrayType',
            measurement_heights: 'mstats.ArrayType'
    ) -> typing.List[float]:
        return list(
            np.array(self.heighted_densities_at(x_values, measurement_heights))
            / np.sum(np.array(measurement_heights))
        )

    def minimum_value(self):
        """
        The lowest measurement value in the distribution

        :return: Minimum measurement value in the distribution
        :rtype: value.ValueUncertainty
        """

        if not len(self.measurements):
            return None

        item = self.measurements[0]
        for v in self.measurements[1:]:
            if v.value == item.value and v.uncertainty > item.uncertainty:
                item = v
            elif v.value < item.value:
                item = v

        return item

    def maximum_value(self):
        """
        The highest measurement value in the distribution

        :return: Maximum measurement value in the distribution
        :rtype: value.ValueUncertainty
        """

        if not len(self.measurements):
            return None

        point = self.measurements[0]
        for m in self.measurements[1:]:
            if m.value == point.value and m.uncertainty > point.uncertainty:
                point = m
            elif m.value > point.value:
                point = m

        return point

    def naked_measurement_values(self, raw=False):
        """
        Returns a list of naked numbers, i.e. without uncertainty values.

        :param raw: (optional) Specifies whether to return raw (not truncated)
            measurement values, or values that have been truncated by their
            uncertainties.
        :type: bool

        :return: A list of naked measurement values
        :rtype: list
        """

        return [(m.raw if raw else m.value) for m in self.measurements]

    def minimum_boundary(self, sigma_threshold):
        """
        The boundary is defined as the value on the measurement (x)
        axis where all measurements are above by at least the specified
        sigma deviation tolerance.

        For example, if we have a distribution with two measurements:
            * m1 = 12 +/- 2
            * m2 = 20 +/- 4
        and we specify sigma_threshold to be 10, then the boundary must be
        the minimum value of:
            * m1: 12 - 2 * 10 = -8
            * m2: 20 - 4 * 10 = -20
        or -20.

        :param sigma_threshold: The threshold number of sigmas deviations that
            all measurements must be above to define the boundary.
        :type: float

        :return: The boundary position at where all measurements reside above
            by at least the specified sigma threshold.
        :rtype: float
        """

        if not len(self.measurements):
            return 0.0
        return min([
            (m.value - float(sigma_threshold) * m.uncertainty)
            for m in self.measurements
        ])

    def maximum_boundary(self, sigma_threshold):
        """
        The boundary is defined as the value on the measurement (x)
        axis where all measurements are below by at least the specified
        sigma deviation tolerance.

        For example, if we have a distribution with two measurements:
            * m1 = 12 +/- 2
            * m2 = 20 +/- 4
        and we specify sigma_threshold to be 10, then the boundary must be
        the maximum value of:
            * m1: 42 + 2 * 10 = 52
            * m2: 20 + 4 * 10 = 60
        or 60.

        :param sigma_threshold: The threshold number of sigmas deviations that
            all measurements must be below to define the boundary.
        :type: float

        :return: The boundary position at where all measurements reside below
            by at least the specified sigma threshold.
        :rtype: float
        """

        if not len(self.measurements):
            return 0.0
        return max([
            (m.value + float(sigma_threshold) * m.uncertainty)
            for m in self.measurements
        ])

