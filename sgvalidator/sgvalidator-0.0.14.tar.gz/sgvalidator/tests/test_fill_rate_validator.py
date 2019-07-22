from unittest import TestCase

import pandas as pd

from ..validators import FillRateValidator
from .utils import getFakeData


class TestTrashValueValidator(TestCase):
    def testFindTrashValues(self):
        fakeData = pd.DataFrame(getFakeData("sample_data_some_columns_null.csv"))
        percBlankDf = fakeData.apply(lambda x: x == "", axis=0).mean() * 100
        nullCountsByColumn = FillRateValidator.validateInner(percBlankDf, "blank")
        expectedConcerningCols = sorted(["zip", "addr", "location_type"])
        self.assertEqual(sorted(list(nullCountsByColumn.index)), expectedConcerningCols)
