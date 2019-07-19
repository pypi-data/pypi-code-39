"""This module adds support for writing test code, like unit sorting, for example. This module is specially useful in
writing sorting for the library itself, but it may be used for other purposes. For instance, take a look at the
:class:compneuro.testing.RandomPatch` class to see how to patch :func:`numpy.random.random`.

.. todo:: Write a minimal unit test suite for this library.
"""

import numpy
import numpy.random
import unittest.mock


class RandomPatch:
    """Patches the :func:`numpy.random.random` function, causing it to cyclically pick values from a given sequence.

    Instances of this class work as context managers that patch the :func:`numpy.random.random`. After entering the
    context, all values will be picked from the sequence of given values, cycling to the start of the sequence whenever
    it is depleted of items for the requested number of items. When the context exits, :func:`numpy.random.random` is
    restored to its original state.

    Parameters
    ----------
    values: typing.Sequence
        Sequence of numbers from where to cyclically draw values.

    Examples
    --------

        >>> from numpy.random import random
        >>> from compneuro.testing import RandomPatch
        >>> values = []
        >>> with RandomPatch([0.1, 0.3, 0.2]):
        ...     values.append(random())
        ...     values.append(random())
        ...     values.append(random(3))
        ...     values.append(random())
        ...
        >>> print(values)
        [0.1, 0.3, 0.2, 0.1, 0.3, 0.2]

    Notes
    -----
    Other functions in the :mod:`numpy.random` module and even in :mod:`math` could be patched by this class, in the
    future.
    """

    def __init__(self, values):
        self.values = values
        self.patched = None
        self.i = 0

    def __enter__(self):
        def random(size=None, **kwargs):
            try:
                value = numpy.array(
                    [
                        self.values[j % len(self.values)]
                        for j in range(self.i, self.i + size)
                    ]
                )
            except TypeError:
                value = self.values[self.i]
            self.i = (self.i + (size or 1)) % len(self.values)
            return value

        self.patched = unittest.mock.patch("numpy.random.random", random)

        return self.patched.__enter__()

    def __exit__(self, *args, **kwargs):
        return self.patched.__exit__(*args, **kwargs)
