import termcolor
from .abstract_validator import AbstractValidator
from .validator_utils import ValidatorUtils


class CentroidValidator(AbstractValidator):
    def __init__(self, data, debug):
        self.data = data
        self.debug = debug

    def announce(self):
        print(termcolor.colored("Checking for centroid quality issues...", "blue"))

    def validate(self):
        for index, row in self.data.iterrows():
            self.validateRow(row)

    def validateRow(self, row):
        latitude = row["latitude"]
        longitude = row["longitude"]

        if ValidatorUtils.is_blank(latitude) and ValidatorUtils.is_blank(longitude):
            return

        if not ValidatorUtils.is_blank(latitude) and ValidatorUtils.is_blank(longitude):
            ValidatorUtils.fail("Latitude without corresponding longitude for row {}".format(row), self.debug)

        if not ValidatorUtils.is_blank(longitude) and ValidatorUtils.is_blank(latitude):
            ValidatorUtils.fail("Longitude without corresponding latitude for row {}".format(row), self.debug)

        if not ValidatorUtils.is_number(latitude):
            ValidatorUtils.fail("Non-numeric latitude: {}".format(latitude), self.debug)
        elif not (-90.0 <= float(latitude) <= 90.0):
            ValidatorUtils.fail("Latitude out of range: {}".format(latitude), self.debug)

        if not ValidatorUtils.is_number(longitude):
            ValidatorUtils.fail("Non-numeric longitude: {}".format(longitude), self.debug)
        elif not (-180.0 <= float(longitude) <= 180.0):
            ValidatorUtils.fail("Longitude out of range: {}".format(longitude), self.debug)
