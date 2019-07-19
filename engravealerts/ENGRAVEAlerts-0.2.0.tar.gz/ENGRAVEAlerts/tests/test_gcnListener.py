import os
import nose2
import shutil
import unittest
import yaml
from ENGRAVEAlerts import gcnListener, cl_utils
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


class test_gcnListener(unittest.TestCase):

    def test_gcnListener_function(self):

        from ENGRAVEAlerts import gcnListener
        this = gcnListener(
            log=log,
            settings=settings,
            test=True
        )
        this.get()

    def test_listen_function(self):

        from ENGRAVEAlerts import gcnListener
        alerts = gcnListener(
            log=log,
            settings=settings
        )
        alerts.listen()

    def test_process_gcn_function(self):

        testEventPacket = pathToInputDir + '/Preliminary-VOEvent.xml'
        from ENGRAVEAlerts import gcnListener
        alerts = gcnListener(
            log=log,
            settings=settings,
            test=True
        )
        alerts.listen(testEventPacket=testEventPacket)

    def test_cache_contacts_function(self):

        from ENGRAVEAlerts import gcnListener
        alerts = gcnListener(
            log=log,
            settings=settings,
            test=True
        )
        alerts.cache_alert_contacts()

    def test_process_gcn_function2(self):

        testEventPacket = pathToInputDir + '/Preliminary-VOEvent.xml'
        from ENGRAVEAlerts import gcnListener
        alerts = gcnListener(
            log=log,
            settings=settings,
            test=True
        )
        alerts.listen(testEventPacket=testEventPacket)

        testEventPacket = pathToInputDir + '/Initial-VOEvent.xml'
        alerts.listen(testEventPacket=testEventPacket)

        testEventPacket = pathToInputDir + '/Update-VOEvent.xml'
        alerts.listen(testEventPacket=testEventPacket)

        testEventPacket = pathToInputDir + '/Retraction-VOEvent.xml'
        alerts.listen(testEventPacket=testEventPacket)

    def test_gcnListener_function_exception(self):

        from ENGRAVEAlerts import gcnListener
        try:
            this = gcnListener(
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
