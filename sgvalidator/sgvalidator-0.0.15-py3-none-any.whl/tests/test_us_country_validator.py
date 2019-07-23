from unittest import TestCase
from ..validators import UsRowValidator

usRowValidator = UsRowValidator(debug=False)


class TestUsCountryChecker(TestCase):
    def testCheckUsState(self):
        usRowValidator.validateState({"state": None})
        usRowValidator.validateState({"state": "ca"})
        usRowValidator.validateState({"state": "CA"})
        usRowValidator.validateState({"state": "California"})
        usRowValidator.validateState({"state": "TX"})
        usRowValidator.validateState({"state": "texas"})

        with self.assertRaises(AssertionError):
            usRowValidator.validateState({"state": "tsxs"})

        with self.assertRaises(AssertionError):
            usRowValidator.validateState({"state": "asds"})

        with self.assertRaises(AssertionError):
            usRowValidator.validateState({"state": "cali"})

        with self.assertRaises(AssertionError):
            usRowValidator.validateState({"state": "sada"})

    def testCheckUsZip(self):
        usRowValidator.validateZip({"zip": "94103"})
        usRowValidator.validateZip({"zip": "94103-1234"})
        usRowValidator.validateZip({"zip": None})

        # note - currently, this zip code doesn't fail because we're
        # not checking against a database of real US zips
        usRowValidator.validateZip({"zip": "00000"})

        with self.assertRaises(AssertionError):
            usRowValidator.validateZip({"zip": "9104"})

        with self.assertRaises(AssertionError):
            usRowValidator.validateZip({"zip": "910421-1234"})

        with self.assertRaises(AssertionError):
            usRowValidator.validateZip({"zip": "342131"})

    def testCheckUsPhone(self):
        usRowValidator.validatePhone({"phone": "2149260428"})
        usRowValidator.validatePhone({"phone": "+12149260428"})
        usRowValidator.validatePhone({"phone": None})
        usRowValidator.validatePhone({"phone": "+1 (214) 926-0428"})

        with self.assertRaises(AssertionError):
            usRowValidator.validatePhone({"phone": "960428"})

        with self.assertRaises(AssertionError):
            usRowValidator.validatePhone({"phone": "214-926!0428"})

        with self.assertRaises(AssertionError):
            usRowValidator.validatePhone({"phone": "2149260428 null"})
