import os
import nose2
import shutil
import unittest
import yaml
from ENGRAVEAlerts import sms, cl_utils
from ENGRAVEAlerts.utKit import utKit

from fundamentals import tools

su = tools(
    arguments={"settingsFile": None},
    docString=__doc__,
    logLevel="DEBUG",
    options_first=False,
    projectName="ENGRAVEAlerts",
    defaultSettingsFile=False
)
arguments, settings, log, dbConn = su.setup()
yaml.warnings({'YAMLLoadWarning': False})

# # load settings
# stream = file(
#     "/Users/Dave/.config/ENGRAVEAlerts/ENGRAVEAlerts.yaml", 'r')
# settings = yaml.load(stream)
# stream.close()

# SETUP AND TEARDOWN FIXTURE FUNCTIONS FOR THE ENTIRE MODULE
moduleDirectory = os.path.dirname(__file__)
utKit = utKit(moduleDirectory)
log, dbConn, pathToInputDir, pathToOutputDir = utKit.setupModule()
utKit.tearDownModule()

# load settings
stream = file(
    "/Users/Dave/Dropbox/config/dave-macbook/ENGRAVEAlerts/ENGRAVEAlerts.yaml", 'r')
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


class test_sms(unittest.TestCase):

    def test_sms_contacts_function(self):

        from ENGRAVEAlerts import sms
        this = sms(
            log=log,
            settings=settings
        )
        this.set_mobile_numbers(
            "+447912626071    +447912626071        +447912626071")
        this.set_mobile_numbers("+447912626071, +447912626071, +447912626071")
        this.set_mobile_numbers("+447912626071")
        this.set_mobile_numbers(
            ["+447912626071", "+447912626071", "+447912626071"])

    def test_sms_sent_function(self):

        from ENGRAVEAlerts import sms
        this = sms(
            log=log,
            settings=settings
        )
        this.set_mobile_numbers("+447912626071, +447912626071, +447912626071")
        this.send_message("this is a unit test from the ENGRAVEAlerts package")

    def test_sms_function_exception(self):

        from ENGRAVEAlerts import sms
        try:
            this = sms(
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
