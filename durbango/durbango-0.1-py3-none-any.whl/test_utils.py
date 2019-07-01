import unittest

import pandas as pd
from pandas.util.testing import assert_frame_equal, assert_series_equal

from .nb_utils import blind_descending_sort


class TestShit(unittest.TestCase):
    def test_blind_descending_sort(self):
        test_df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]}, index=[0, 1])
        assert_frame_equal(test_df.pipe(blind_descending_sort),  # intentional use of pipe
                           test_df.sort_values('a', ascending=False))
        test_ser = test_df['b']
        assert_series_equal(test_ser.pipe(blind_descending_sort),  # intentional use of pipe
                            test_df['b'].sort_values(ascending=False))

        # MultiIndex
        test_df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]}, index=[0, 1])
        test_df.columns = pd.MultiIndex.from_tuples([('a', 'ANOTHER LEVEL'), ('b', 'ANOTHER')])
        assert_frame_equal(test_df.pipe(blind_descending_sort),  # intentional use of pipe
                           test_df.sort_values(('a', 'ANOTHER LEVEL'), ascending=False))
        # Bad Inputs
        with self.assertRaises(AttributeError):
            blind_descending_sort([1, 2, 3, 4])

    # TODO(SS): test_tar_compress
