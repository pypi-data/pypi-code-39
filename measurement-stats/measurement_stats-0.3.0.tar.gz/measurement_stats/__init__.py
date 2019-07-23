import typing as _typing
import numpy as _np

from measurement_stats import angle
from measurement_stats import mean
from measurement_stats import ops
from measurement_stats import value
from measurement_stats.value import ValueUncertainty
from measurement_stats import value2D
from measurement_stats import values
from measurement_stats import distributions
from measurement_stats.distributions import Distribution
from measurement_stats.distributions import create_distribution

ArrayType = _typing.Union[
    _np.array,
    list,
    tuple,
    _typing.Generator,
    _typing.Iterable
]
