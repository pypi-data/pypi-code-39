from types import GeneratorType
from itertools import tee
from collections import OrderedDict

import numpy as np

from jsondler.json_tools import columnize_dicts_list


class ColsDict(OrderedDict):
    """

    """

    def __init__(self, seq=None, **kwargs):
        seq = ColsDict._prepare_seq(seq=seq)
        super(ColsDict, self).__init__(seq, **kwargs)
        self._columns = list(map(lambda it: it[0], seq))

    @staticmethod
    def _prepare_seq(seq):
        if type(seq) in (list, tuple, GeneratorType):
            types_set = set()
            seq, seq_ = tee(seq)
            for it in range(100):
                types_set.add(type(next(seq_)))
            types_list = list(types_set)
            if len(types_list) == 1 and types_list[0] is dict:
                seq = columnize_dicts_list(seq, na=np.nan).items()
        return seq

    @property
    def columns(self):
        keys = self.keys()
        c_i = 0
        while c_i < len(self._columns):
            if self._columns[c_i] not in keys:
                self._columns.pop(c_i)
            else:
                c_i += 1
        for key in keys:
            if key not in self._columns:
                self._columns.append(key)
        return self._columns

    def append_row(self, row):
        pass

    def insert_row(self, i, row):
        pass

    def pop_row(self, i):
        pass

    def rearrange_cols(self, ordered_cols):
        self._columns = ordered_cols

    def rename_cols(self, rename_dict):
        for old_col in rename_dict:
            self[rename_dict[old_col]] = self.pop(old_col)

    def values(self):
        cols_array = np.array([self[col] for col in self.columns])
        return np.transpose(cols_array)

    def fillna(self, na):
        pass

    @property
    def shape(self):
        return len(self[self.columns[0]]), len(self.columns)
