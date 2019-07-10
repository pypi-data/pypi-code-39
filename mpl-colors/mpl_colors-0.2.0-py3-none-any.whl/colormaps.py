from random import Random
from typing import Union, Tuple
from copy import deepcopy

import numpy as np
from matplotlib.colors import Colormap, colorConverter


RgbaIorF = Union[
    Tuple[float, float, float, float],
    Tuple[int, int, int, int],
]


class LabelColorMap(Colormap):
    """Colormap class which turns integers into a random (deterministic) RGB tuple"""
    name = "label"

    def __init__(self, seed=0):
        super().__init__(self.name)
        self.seed = int(seed)

    def __call__(self, X, alpha=None, bytes=False) -> Union[RgbaIorF, np.ndarray]:
        if alpha is None:
            alpha = 1
        else:
            alpha = np.clip(alpha, 0, 1)

        is_scalar = np.isscalar(X)

        if is_scalar:
            arr = np.ma.array([X])
        else:
            is_scalar = False
            arr = np.ma.array(X, copy=True)

        out = np.repeat(np.array([self._rgba_bad], dtype=float), repeats=arr.size, axis=0).reshape(arr.shape + (4,))

        col = np.array([0, 0, 0, alpha], dtype=float)
        uniques = np.unique(arr.compressed())

        for val in uniques:
            rand = Random(val + self.seed)
            col[:3] = [rand.random() for _ in range(3)]
            out[np.logical_and(arr == val, ~arr.mask), :] = col

        if bytes:
            out = (out * 255).astype(np.dtype('uint8'))

        if is_scalar:
            out = tuple(out.squeeze())

        return out

    def __copy__(self):
        return deepcopy(self)

    def set_bad(self, color='k', alpha=None):
        """Set color to be used for masked values.
        """
        self._rgba_bad = colorConverter.to_rgba(color, alpha)

    def set_under(self, color='k', alpha=None):
        """Set color to be used for low out-of-range values.
           Requires norm.clip = False
        """
        raise NotImplementedError()

    def set_over(self, color='k', alpha=None):
        """Set color to be used for high out-of-range values.
           Requires norm.clip = False
        """
        raise NotImplementedError()

    def is_gray(self):
        return False

    def _init(self):
        raise NotImplementedError()

    def _resample(self, lutsize):
        raise NotImplementedError()

    def reversed(self, name=None):
        raise NotImplementedError()
