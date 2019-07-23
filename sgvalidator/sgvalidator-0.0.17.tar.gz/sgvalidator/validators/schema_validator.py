import termcolor

from .abstract_validator import AbstractValidator
from .validator_utils import ValidatorUtils


class SchemaValidator(AbstractValidator):
    def __init__(self, data, rawData, debug):
        self.data = data
        self.rawData = rawData
        self.debug = debug
        self.requiredColumns = {"locator_domain", "location_name", "street_address", "city", "state", "zip",
                                "country_code", "store_number", "phone", "location_type", "latitude", "longitude",
                                "hours_of_operation"}

    def announce(self):
        print(termcolor.colored("Checking for schema issues...", "blue"))

    def validate(self):
        requiredColsNotInData = self.getRequiredColumnsThatArentInData()
        if len(requiredColsNotInData) > 0:
            # debug = False because we need to fail no matter what if the schema is wrong
            ValidatorUtils.fail("Data does not contain the following required columns {}.\n"
                                "Failing because the remainder of the checks won't be able to complete.\n"
                                .format(requiredColsNotInData), debug=False)

        # todo - transition this to pandas
        for row in self.rawData:
            for column in row:
                if type(row[column]) not in [type(None), type(''), type(u''), type(0), type(0.0), type(True)]:
                    message = "row {} contains unexpected data type {}".format(row, type(row[column]))
                    ValidatorUtils.fail(message, self.debug)

    def getRequiredColumnsThatArentInData(self):
        return self.requiredColumns.difference(self.data.columns)