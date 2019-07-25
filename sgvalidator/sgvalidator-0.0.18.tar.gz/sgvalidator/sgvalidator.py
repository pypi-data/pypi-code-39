import os
import csv
import json
import termcolor
from glob import glob
from .validator_runner import ValidatorRunner

VERSION = "0.0.18"  # make sure this is consistent with setup.py


def validate(dataLocation, debug=False):
    data = Validator.readDataFromLocation(dataLocation)
    Validator.validate(data, debug)
    Validator.optionallyWriteSuccessFile(debug)


class Validator:
    SUCCESS_FILEPATH = './SUCCESS'

    @staticmethod
    def readDataFromLocation(dataLocation):
        data = []
        if dataLocation.endswith(".csv"):
            with open(dataLocation) as csv_file:
                reader = csv.DictReader(csv_file, skipinitialspace=True)
                for row in reader:
                    data.append(row)
        else:
            for f_name in glob(os.path.join(dataLocation, 'datasets/default', '*.json')):
                with open(f_name) as json_file:
                    data.append(json.load(json_file))

        if len(data) == 0:
            message = "Data location doesn't exist or dataset is empty: {}".format(dataLocation)
            print(termcolor.colored(message, "red"))
            exit(0)

        return data

    @staticmethod
    def optionallyWriteSuccessFile(debug):
        if not debug:
            message = termcolor.colored("Woohoo! Creating SUCCESS file. Please commit this with your scraper.", "green")
            print(message)
            Validator.touch(Validator.SUCCESS_FILEPATH)
            with open(Validator.SUCCESS_FILEPATH, 'a') as f:
                f.write(VERSION)

    @staticmethod
    def touch(path):
        with open(path, 'a'):
            os.utime(path, None)

    @staticmethod
    def validate(data, debug):
        print(termcolor.colored("Validating data with DEBUG = {}".format(debug), "green"))
        checks = ValidatorRunner(data, debug)
        checks.run()
