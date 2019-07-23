import termcolor
from .abstract_validator import AbstractValidator
from .country_validation_helpers.country_detector import CountryDetector
from .country_validation_helpers.us_row_validator import UsRowValidator
from .country_validation_helpers.ca_row_validator import CaRowValidator


class CountryValidator(AbstractValidator):
    def __init__(self, data, debug):
        self.data = data
        self.debug = debug
        self.caRowValidator = CaRowValidator(debug)
        self.usRowValidator = UsRowValidator(debug)

    def announce(self):
        print(termcolor.colored("Validating country-specific information (states, zip codes, phone #'s)...", "blue"))

    def validate(self):
        for index, row in self.data.iterrows():
            detectedCountryCode = CountryDetector.detect(row)
            self.validateRow(row, detectedCountryCode)

    def validateRow(self, row, detectedCountryCode):
        if detectedCountryCode == CountryDetector.US_COUNTRY_CODE:
            self.usRowValidator.validate(row)
        elif detectedCountryCode == CountryDetector.CA_COUNTRY_CODE:
            self.caRowValidator.validate(row)
