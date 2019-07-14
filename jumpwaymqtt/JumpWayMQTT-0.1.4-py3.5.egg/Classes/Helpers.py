############################################################################################
#
# Software:      iotJumpWay MQTT Python Clients
# Author:        Adam Milton-Barker (AdamMiltonBarker.com)
# License:       Eclipse Public License 2.0
#
# Title:         iotJumpWay MQTT Python Client Helpers
# Description:   Helpers class providing common helper functions to the iotJumpWay MQTT 
#                Python Clients.
# Last Modified: 2019-04-07
#
############################################################################################

import os, json, requests, hashlib, hmac, base64

from requests.auth import HTTPBasicAuth

class Helpers():

    def __init__(self):

        """ Initiates the Helpers class """

        pass

    def setLogFile(self, path):

        """ Sets a log file path """

        if not os.path.exists(path):
            os.makedirs(path)
        
        return path + datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S') + ".txt"
        
    def logMessage(self, logfile, process, messageType, message, hide = False):

        """
        Logs a message to a log file
        """

        logString = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + "|" + process + "|" + messageType + "|" + message
        with open(logfile,"a") as logLine:
            logLine.write(logString+'\r\n')
        if hide == False:
            print(logString)