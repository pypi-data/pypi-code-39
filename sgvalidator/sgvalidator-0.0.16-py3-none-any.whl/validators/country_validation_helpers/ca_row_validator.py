from .country_detector import CountryDetector
from ..validator_utils import ValidatorUtils
from .abstract_country_validator import AbstractCountryValidator


class CaRowValidator(AbstractCountryValidator):
    def __init__(self, debug):
        self.debug = debug

    def validate(self, row):
        self.validateZip(row)
        self.validateState(row)
        self.validatePhone(row)

    def validateState(self, row):
        state = row["state"]
        if not ValidatorUtils.is_blank(state) and not CountryDetector.isCaState(state):
            ValidatorUtils.fail("Invalid Canadian province/territory: {}".format(state), self.debug)

    def validatePhone(self, row):
        phone = row["phone"]
        if not ValidatorUtils.is_blank(phone) and not ValidatorUtils.is_valid_phone_number(phone, "CA"):
            ValidatorUtils.fail("Invalid Canadian phone number: {}".format(phone), self.debug)

    def validateZip(self, row):
        zip_code = row["zip"]
        if not ValidatorUtils.is_blank(zip_code) and not CountryDetector.isCaZip(zip_code):
            ValidatorUtils.fail("Invalid Canadian postal code: {}".format(zip_code), self.debug)