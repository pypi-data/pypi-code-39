import pandas as pd
from unittest import TestCase
from .utils import getFakeData
from ..validators import SchemaValidator


class TestSchemaValidator(TestCase):
    def testCheckSchema(self):
        goodData = getFakeData('sample_data_good_header.csv')
        checkerGood = SchemaValidator(pd.DataFrame(goodData), goodData, debug=False)
        checkerGood.validate()

        badData = getFakeData('sample_data_bad_header.csv')
        checkerBad = SchemaValidator(pd.DataFrame(badData), badData, debug=False)

        self.assertTrue(len(checkerGood.getRequiredColumnsThatArentInData()) == 0)
        self.assertTrue(checkerBad.getRequiredColumnsThatArentInData() == {"street_address", "state"})
        with self.assertRaises(AssertionError):
            checkerBad.validate()

