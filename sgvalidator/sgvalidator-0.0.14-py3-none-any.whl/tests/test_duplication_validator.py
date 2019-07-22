from unittest import TestCase

import pandas as pd

from ..validators import DuplicationValidator
from .utils import getFakeData

data = pd.DataFrame(getFakeData())
debugChecker = DuplicationValidator(data, debug=True)
nonDebugChecker = DuplicationValidator(data, debug=False)


class TestDuplicationChecker(TestCase):
    def testCheckIdentityDuplication(self):
        self.assertTrue(len(debugChecker.validateIdentityDuplicates() == 3))
        with self.assertRaises(AssertionError):
            nonDebugChecker.validate()

    def testCheckLatLngDuplication(self):
        self.assertTrue(len(debugChecker.validateLatLngsWithMultipleAddresses() == 1))
        with self.assertRaises(AssertionError):
            nonDebugChecker.validate()

    def testWarnIfSameAddrHasMultipleLatLngs(self):
        res = debugChecker.warnIfSameAddrHasMultipleLatLngs()
        self.assertTrue(len(res) == 2)