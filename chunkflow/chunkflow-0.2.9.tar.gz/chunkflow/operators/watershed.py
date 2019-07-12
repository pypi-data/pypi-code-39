import numpy as np

from .operator_base import OperatorBase


class WatershedOperator(OperatorBase):
    def __init__(self, name: str='watershed', verbose: bool=True):
        super().__init__(name=name, verbose=verbose)
        import mutex_watershed as mw


    def __call__(self, chunk, seg=None):
        """run mutex watershed to segment affinity map."""
        assert isinstance(chunk, np.ndarray)

