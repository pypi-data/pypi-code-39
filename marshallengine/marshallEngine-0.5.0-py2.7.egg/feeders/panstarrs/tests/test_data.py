import os
import nose2
import shutil
import unittest
import yaml
from marshallEngine.utKit import utKit

from fundamentals import tools

su = tools(
    arguments={"settingsFile": None},
    docString=__doc__,
    logLevel="DEBUG",
    options_first=False,
    projectName="marshallEngine",
    defaultSettingsFile=False
)
arguments, settings, log, dbConn = su.setup()

# # load settings
# stream = file(
#     "/Users/Dave/.config/marshallEngine/marshallEngine.yaml", 'r')
# settings = yaml.load(stream)
# stream.close()

# SETUP AND TEARDOWN FIXTURE FUNCTIONS FOR THE ENTIRE MODULE
moduleDirectory = os.path.dirname(__file__)
utKit = utKit(moduleDirectory)
log2, dbConn2, pathToInputDir, pathToOutputDir = utKit.setupModule()
utKit.tearDownModule()

# load settings
from os.path import expanduser
home = expanduser("~")
stream = file(
    home + "/.config/marshallEngine/marshallEngine.yaml", 'r')
settings = yaml.load(stream)
stream.close()

import shutil
try:
    shutil.rmtree(pathToOutputDir)
except:
    pass
# COPY INPUT TO OUTPUT DIR
shutil.copytree(pathToInputDir, pathToOutputDir)

# Recursively create missing directories
if not os.path.exists(pathToOutputDir):
    os.makedirs(pathToOutputDir)

# xt-setup-unit-testing-files-and-folders


class test_data(unittest.TestCase):

    def test_data_function(self):

        from marshallEngine.feeders.panstarrs.data import data
        ingesters = data(
            log=log,
            settings=settings,
            dbConn=dbConn
        )
        csvDicts = ingesters.get_csv_data(
            url=settings["panstarrs urls"]["ps13pi"]["summary csv"],
            user=settings["credentials"]["ps13pi"]["username"],
            pwd=settings["credentials"]["ps13pi"]["password"]
        )
        ingesters._clean_data_pre_ingest(
            surveyName="ps13pi", withinLastDays=50)
        ingesters._import_to_feeder_survey_table()
        ingesters.get_csv_data(
            url=settings["panstarrs urls"]["ps13pi"]["recurrence csv"],
            user=settings["credentials"]["ps13pi"]["username"],
            pwd=settings["credentials"]["ps13pi"]["password"]
        )
        ingesters._clean_data_pre_ingest(
            surveyName="ps13pi", withinLastDays=50)
        ingesters._import_to_feeder_survey_table()
        ingesters.insert_into_transientBucket()

    def test_data_function2(self):

        from marshallEngine.feeders.panstarrs.data import data
        ingesters = data(
            log=log,
            settings=settings,
            dbConn=dbConn
        )
        csvDicts = ingesters.get_csv_data(
            url=settings["panstarrs urls"]["pso3"]["summary csv"],
            user=settings["credentials"]["pso3"]["username"],
            pwd=settings["credentials"]["pso3"]["password"]
        )
        data = ingesters._clean_data_pre_ingest(
            surveyName="pso3", withinLastDays=50)
        ingesters._import_to_feeder_survey_table()
        ingesters.get_csv_data(
            url=settings["panstarrs urls"]["pso3"]["recurrence csv"],
            user=settings["credentials"]["pso3"]["username"],
            pwd=settings["credentials"]["pso3"]["password"]
        )
        ingesters._clean_data_pre_ingest(surveyName="pso3", withinLastDays=50)
        ingesters._import_to_feeder_survey_table()
        ingesters.insert_into_transientBucket()

    def test_data_function_exception(self):

        from marshallEngine import data
        try:
            this = data(
                log=log,
                settings=settings,
                fakeKey="break the code"
            )
            this.get()
            assert False
        except Exception, e:
            assert True
            print str(e)

        # x-print-testpage-for-pessto-marshall-web-object

    # x-class-to-test-named-worker-function
