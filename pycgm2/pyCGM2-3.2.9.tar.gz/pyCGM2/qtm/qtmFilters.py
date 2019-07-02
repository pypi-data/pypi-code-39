import logging
import pyCGM2
from pyCGM2.Utils import files


from pyCGM2.Tools import btkTools

import sys
import os
import json
sys.path.append( "C:\Users\HLS501\Documents\Programming\API\pyCGM2\pyCGM2\pyCGM2\qtm\gaitWebReport")
import parserUploader


class WebReportFilter(object):
    def __init__(self,workingDirectory):

        if os.path.isfile(os.getcwd() + '/config.json'):
            with open(os.getcwd() + '/config.json') as jsonDataFile:
                configData = json.load(jsonDataFile)
        else:
            print "Config.json not found at " + os.getcwd()


        self.processing = parserUploader.ParserUploader(workingDirectory,configData)


    def exportJson(self):

        jsonData = self.processing.createReportJson()

        files.saveJson("","jsonData.json",jsonData)


    def upload(self):

        self.processing.Upload()






if __name__=="__main__":

    workingDirectory = "C:\\Users\\HLS501\\Documents\\Programming\\API\\pyCGM2\\pyCGM2-Qualisys\\Data\WebReport\\"
    report =  WebReportFilter(workingDirectory)
    report.exportJson()

    report.upload()
