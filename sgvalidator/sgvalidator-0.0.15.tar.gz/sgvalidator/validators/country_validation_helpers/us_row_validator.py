import us
from .abstract_country_validator import AbstractCountryValidator
from .country_detector import CountryDetector
from ..validator_utils import ValidatorUtils


class UsRowValidator(AbstractCountryValidator):
    def __init__(self, debug):
        self.debug = debug

    def validate(self, row):
        self.validateZip(row)
        self.validateState(row)
        self.validatePhone(row)

    def validateState(self, row):
        state = row["state"]
        if not ValidatorUtils.is_blank(state) and not us.states.lookup(state.strip()):
            ValidatorUtils.fail("Invalid state: {}".format(state), self.debug)

    def validateZip(self, row):
        zip_code = row["zip"]
        if not ValidatorUtils.is_blank(zip_code) and not CountryDetector.isUsZip(zip_code):
            ValidatorUtils.fail("Invalid zip code: {}".format(zip_code), self.debug)

    def validatePhone(self, row):
        phone = row["phone"]
        if not ValidatorUtils.is_blank(phone) and not ValidatorUtils.is_valid_phone_number(phone, "US"):
            ValidatorUtils.fail("Invalid phone number: {}".format(phone), self.debug)