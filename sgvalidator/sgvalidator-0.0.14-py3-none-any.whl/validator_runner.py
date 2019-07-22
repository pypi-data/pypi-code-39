import pandas as pd
from .validators.centroid_validator import CentroidValidator
from .validators.country_validator import CountryValidator
from .validators.duplication_validator import DuplicationValidator
from .validators.fill_rate_validator import FillRateValidator
from .validators.schema_validator import SchemaValidator
from .validators.trash_value_validator import TrashValueValidator


class ValidatorRunner:
    def __init__(self, data, debug):
        self.rawData = data
        self.data = pd.DataFrame(data)
        self.debug = debug
        self.validators = [
            SchemaValidator(self.data, self.rawData, self.debug),  # todo - move this off of raw data
            DuplicationValidator(self.data, self.debug),
            CentroidValidator(self.data, self.debug),
            CountryValidator(self.data, self.debug),
            TrashValueValidator(self.data, self.debug),
            FillRateValidator(self.data)
        ]

    def run(self):
        for validator in self.validators:
            validator.announce()
            validator.validate()
