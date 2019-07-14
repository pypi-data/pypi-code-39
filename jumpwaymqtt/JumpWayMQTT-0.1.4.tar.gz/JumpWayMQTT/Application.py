############################################################################################
#
# Software:      iotJumpWay MQTT Python Clients
# Author:        Adam Milton-Barker (AdamMiltonBarker.com)
# License:       Eclipse Public License 2.0
#
# Title:         iotJumpWay MQTT Python JumpWay Application Client
# Description:   An iotJumpWay MQTT Python JumpWay Application Client that allows you to
#                connect to the iotJumpWay.
# Last Modified: 2019-04-07
#
############################################################################################

import os
import sys
import time
import json

import paho.mqtt.client as mqtt

from Classes.Helpers import Helpers


class JumpWayApp():

    __version__ = "0.1.5"

    def __init__(self, params):
        """ inits the iotJumpWay JumpWayApp class """

        self.parameters = params

        self.Helpers = Helpers()
        self.LogDir = os.getcwd() + "/Logs/Applications/"
        self.LogFile = self.Helpers.setLogFile(self.LogDir)

        self.Helpers.logMessage(self.LogFile, "JumpWayApp", "init",
                                "JumpWayMQTT JumpWayApp logs initiated!")

        self.checkParameters()
        self.initMQTT()
        self.initCallbacks()

        self.Helpers.logMessage(self.LogFile, "JumpWayApp", "init",
                                "JumpWayMQTT JumpWayApp initiated!")

    def checkParameters(self):
        """ Validates required incoming parameters """

        exitApp = False
        msg = ""

        if self.parameters['JumpWayLocID'] is None:
            msg = "JumpWayMQTT Location ID (JumpWayLocID) parameter is required!"
            exitApp = True
        elif self.parameters['JumpWayAppID'] is None:
            msg = "JumpWayMQTT JumpWayApp ID (JumpWayAppID) parameter is required!"
            exitApp = True
        elif self.parameters['JumpWayAppName'] is None:
            msg = "JumpWayMQTT JumpWayApp name (JumpWayAppName) parameter is required!"
            exitApp = True
        elif self.parameters['username'] is None:
            msg = "JumpWayMQTT JumpWayApp MQTT username (username) parameter is required!"
            exitApp = True
        elif self.parameters['password'] is None:
            msg = "JumpWayMQTT JumpWayApp MQTT password (password) parameter is required!"
            exitApp = True

        if exitApp is True:
            self.Helpers.logMessage(
                self.LogFile, "JumpWayApp", "checkParameters", msg)
            sys.exit()
        else:
            self.Helpers.logMessage(self.LogFile, "JumpWayApp", "checkParameters",
                                    "JumpWayMQTT JumpWayApp parameters OK!")

    def initMQTT(self):
        """ inits the iotJumpWay JumpWayApp MQTT Client """

        self.mqttClient = None
        self.mqttTLS = os.path.dirname(
            os.path.abspath(__file__)) + "/CA/ca.pem"
        self.mqttHost = 'iot.techbubbletechnologies.com'
        self.mqttPort = 8883

        self.Helpers.logMessage(self.LogFile, "JumpWayApp", "initMQTT",
                                "JumpWayMQTT JumpWayApp MQTT Client initiated!")

    def initCallbacks(self):
        """ inits the iotJumpWay JumpWayApp MQTT Callback functions """

        self.appStsCbck = None
        self.appHdwrCbck = None
        self.appNtfCbck = None
        self.appWrnCbck = None
        self.appSnsCbck = None
        self.appActCbck = None
        self.appCmmdCbck = None
        self.dvcStsCbck = None
        self.dvcHdwrCbck = None
        self.dvcNtfCbck = None
        self.dvcWrnCbck = None
        self.dvcSnsCbck = None
        self.dvcActCbck = None
        self.dvcCmmdCbck = None

        self.Helpers.logMessage(self.LogFile, "JumpWayApp", "initCallbacks",
                                "JumpWayMQTT JumpWayApp MQTT Callbacks initiated!")

    def appCxn(self):
        """ inits an iotJumpWay JumpWayApp MQTT connection """

        try:
            self.mqttClient = mqtt.Client(
                client_id=self.parameters['JumpWayAppName'], clean_session=True)
            appStatusTopic = '%s/Applications/%s/Status' % (
                self.parameters['JumpWayLocID'], self.parameters['JumpWayAppID'])
            self.mqttClient.will_set(appStatusTopic, "OFFLINE", 0, False)
            self.mqttClient.tls_set(self.mqttTLS, certfile=None, keyfile=None)
            self.mqttClient.on_connect = self.onAppCxn
            self.mqttClient.on_subscribe = self.onAppSub
            self.mqttClient.on_message = self.onMessage
            self.mqttClient.on_publish = self.onAppPub
            self.mqttClient.username_pw_set(
                str(self.parameters['username']), str(self.parameters['password']))
            self.mqttClient.connect(self.mqttHost, self.mqttPort, 10)
            self.mqttClient.loop_start()
            time.sleep(4)

            self.Helpers.logMessage(self.LogFile, "JumpWayApp", "appCxn",
                                    "JumpWayMQTT JumpWayApp MQTT Connection initiated!")
        except Exception as e:
            self.Helpers.logMessage(self.LogFile, "JumpWayApp", "appCxn",
                                    "JumpWayMQTT JumpWayApp MQTT Connection initiation failed! " + str(e))
            exit()

    def onAppCxn(self, client, obj, flags, rc):
        """ Triggered on successfull iotJumpWay JumpWayApp MQTT connection """

        self.appStsPub("ONLINE")
        self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onAppCxn",
                                "JumpWayMQTT JumpWayApp Connected successfully! RC: " + str(rc))

    def onAppSub(self, client, obj, mid, granted_qos):
        """ Triggered on successfull iotJumpWay JumpWayApp MQTT subscription """

        self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onAppSub",
                                "JumpWayMQTT JumpWayApp subscribe: " + str(obj) + " " + str(mid) + " " + str(granted_qos))

    def appTpcSub(self, JumpWayAppID, topicID, qos=0):
        """ Subscribes to an iotJumpWay JumpWayApp MQTT topic """

        if self.parameters['JumpWayLocID'] is None:
            self.Helpers.logMessage(self.LogFile, "JumpWayApp", "appTpcSub",
                                    "JumpWayMQTT JumpWayApp Location ID (locationID) required!")
            return False
        elif JumpWayAppID is None:
            self.Helpers.logMessage(self.LogFile, "JumpWayApp", "appTpcSub",
                                    "JumpWayMQTT JumpWayApp ID (JumpWayAppID) required!")
            return False
        elif topicID is None:
            self.Helpers.logMessage(self.LogFile, "JumpWayApp", "appTpcSub",
                                    "JumpWayMQTT JumpWayApp Topic ID (topicID) required!")
            return False
        else:
            if JumpWayAppID is "All":
                appTpc = '%s/Applications/#' % (
                    self.parameters['JumpWayLocID'])
                self.mqttClient.subscribe(appTpc, qos=qos)
                self.Helpers.logMessage(self.LogFile, "JumpWayApp", "appTpcSub",
                                        "JumpWayMQTT JumpWayApp subscribed to ALL JumpWayApp topics!")
            else:
                appTpc = '%s/Applications/%s/%s' % (
                    self.parameters['JumpWayLocID'], JumpWayAppID, topicID)
                self.mqttClient.subscribe(appTpc, qos=qos)
                self.Helpers.logMessage(self.LogFile, "JumpWayApp", "appTpcSub",
                                        "JumpWayMQTT JumpWayApp subscribed to JumpWayApp " + str(JumpWayAppID) + " topic " + str(topicID) + "!")

    def dvcTpcSub(self, zone, device, topicID, qos=0):
        """ Subscribes to an iotJumpWay Device MQTT topic """

        if self.parameters['JumpWayLocID'] is None:
            self.Helpers.logMessage(self.LogFile, "JumpWayApp", "dvcTpcSub",
                                    "JumpWayMQTT JumpWayApp Device " + str(dvc) + " Location ID (locationID) required!")
            return False
        elif zone is None:
            self.Helpers.logMessage(self.LogFile, "JumpWayApp", "dvcTpcSub",
                                    "JumpWayMQTT JumpWayApp Device " + str(dvc) + " Zone ID (zoneID) required!")
            return False
        elif device is None:
            self.Helpers.logMessage(self.LogFile, "JumpWayApp", "dvcTpcSub",
                                    "JumpWayMQTT JumpWayApp Device " + str(dvc) + " ID (device) required!")
            return False
        elif topicID is None:
            self.Helpers.logMessage(self.LogFile, "JumpWayApp", "dvcTpcSub",
                                    "JumpWayMQTT JumpWayApp Device " + str(dvc) + " Topic ID (topicID) required!")
            return False
        else:
            if device is "All":
                dvcTpc = '%s/Devices/#' % (self.parameters['JumpWayLocID'])
                self.mqttClient.subscribe(dvcTpc, qos=qos)
                self.Helpers.logMessage(self.LogFile, "JumpWayApp", "dvcTpcSub",
                                        "JumpWayMQTT JumpWayApp subscribed to ALL Device topics")
            else:
                dvcTpc = '%s/Devices/%s/%s/%s' % (
                    self.parameters['JumpWayLocID'], zone, device, topic)
                self.mqttClient.subscribe(dvcTpc, qos=qos)
                self.Helpers.logMessage(self.LogFile, "JumpWayApp", "dvcTpcSub",
                                        "JumpWayMQTT JumpWayApp subscribed to Device " + str(device) + " topic " + str(topicID))

    def onAppPub(self, client, obj, mid):
        """ Triggered on successfull iotJumpWay JumpWayApp MQTT publish """

        self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onAppPub",
                                "JumpWayMQTT JumpWayApp publish: " + str(mid))

    def appStsPub(self, data):
        """ Publishes iotJumpWay JumpWayApp MQTT JumpWayApp status message """

        if self.parameters['JumpWayLocID'] is None:
            self.Helpers.logMessage(self.LogFile, "JumpWayApp", "appStsPub",
                                    "JumpWayMQTT JumpWayApp Location ID (locationID) required!")
            return False
        elif self.parameters['JumpWayAppID'] is None:
            self.Helpers.logMessage(self.LogFile, "JumpWayApp", "appStsPub",
                                    "JumpWayMQTT JumpWayApp ID (JumpWayAppID) required!")
            return False
        else:
            dvcStsTopic = '%s/Applications/%s/Status' % (
                self.parameters['JumpWayLocID'], self.parameters['JumpWayAppID'])
            self.mqttClient.publish(dvcStsTopic, data)
            self.Helpers.logMessage(self.LogFile, "JumpWayApp", "appStsPub",
                                    "JumpWayMQTT JumpWayApp successfully published to topic: " + dvcStsTopic)

    def appTpcPub(self, topic, data):
        """ Publishes iotJumpWay JumpWayApp MQTT JumpWayApp message to desired topic """

        if self.parameters['JumpWayLocID'] is None:
            self.Helpers.logMessage(self.LogFile, "JumpWayApp", "appTpcPub",
                                    "JumpWayMQTT JumpWayApp Location ID (locationID) required!")
            return False
        elif self.parameters['JumpWayAppID'] is None:
            self.Helpers.logMessage(self.LogFile, "JumpWayApp", "appTpcPub",
                                    "JumpWayMQTT JumpWayApp ID (JumpWayAppID) required!")
            return False
        else:
            appTpc = '%s/Applications/%s/%s' % (
                self.parameters['JumpWayLocID'], self.parameters['JumpWayAppID'], topic)
            self.mqttClient.publish(appTpc, json.dumps(data))
            self.Helpers.logMessage(self.LogFile, "JumpWayApp", "appTpcPub",
                                    "JumpWayMQTT JumpWayApp successfully published to topic: " + appTpc)

    def dvcTpcPub(self, topic, zone, device, data):
        """ Publishes iotJumpWay JumpWayApp MQTT device message to desired topic """

        if self.parameters['JumpWayLocID'] is None:
            self.Helpers.logMessage(self.LogFile, "JumpWayApp", "dvcTpcPub",
                                    "JumpWayMQTT Device Location ID (locationID) required!")
            return False
        elif zone is None:
            self.Helpers.logMessage(self.LogFile, "JumpWayApp", "dvcTpcPub",
                                    "JumpWayMQTT Device Zone ID (zoneID) required!")
            return False
        elif device is None:
            self.Helpers.logMessage(self.LogFile, "JumpWayApp", "dvcTpcPub",
                                    "JumpWayMQTT Device ID (device) required!")
            return False
        else:
            dvctopic = '%s/Devices/%s/%s/%s' % (
                self.parameters['JumpWayLocID'], zone, device, topic)
            self.mqttClient.publish(dvctopic, json.dumps(data))
            self.Helpers.logMessage(self.LogFile, "JumpWayApp", "dvcTpcPub",
                                    "JumpWayMQTT JumpWayApp published to Device " + str(device) + " topic " + str(topic))

    def onMessage(self, client, obj, msg):
        """ Triggered on receiving iotJumpWay JumpWayApp MQTT message """

        tpc = msg.topic
        stpc = tpc.split("/")

        self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                "JumpWayMQTT JumpWayApp message received from " + tpc + " activity")

        if stpc[1] == 'Applications':
            if stpc[3] == 'Status':
                if self.appStsCbck is None:
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Status callback (appStsCbck) required!")
                else:
                    self.appStsCbck(msg.topic, msg.payload)
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Status callback initiated!")
            elif stpc[3] == 'Hardware':
                if self.appHdwrCbck is None:
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Hardware callback (appHdwrCbck) required!")
                else:
                    self.dvcHdwrCbck(msg.topic, msg.payload)
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Hardware callback initiated!")
            elif stpc[3] == 'Notifications':
                if self.appNtfCbck is None:
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Notification callback (appNtfCbck) required!")
                else:
                    self.appNtfCbck(msg.topic, msg.payload)
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Notification callback (appNtfCbck) initiated!")
            elif stpc[3] == 'Warnings':
                if self.appWrnCbck is None:
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Warning callback (appWrnCbck) required!")
                else:
                    self.appWrnCbck(msg.topic, msg.payload)
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Warning callback (appWrnCbck) initiated!")
            elif stpc[3] == 'Sensors':
                if self.appSnsCbck is None:
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Sensor callback (appSnsCbck) required!")
                else:
                    self.dvcSnsCbck(msg.topic, msg.payload)
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Sensor callback (appSnsCbck) initiated!")
            elif stpc[4] == 'Actuators':
                if self.appActCbck is None:
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Actuator callback (appActCbck) required!")
                else:
                    self.appActCbck(msg.topic, msg.payload)
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Actuator callback (appActCbck) initiated!")
            elif stpc[3] == 'Commands':
                if self.appCmmdCbck is None:
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Command callback (appCmmdCbck) required!")
                else:
                    self.appCmmdCbck(msg.topic, msg.payload)
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Command callback (appCmmdCbck) initiated!")
        elif stpc[1] == 'Devices':
            if stpc[4] is 'Status':
                if self.dvcStsCbck is None:
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Device Status callback (dvcStsCbck) required!")
                else:
                    self.dvcStsCbck(msg.topic, msg.payload)
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Device Status callback (dvcStsCbck) initiated!")
            elif stpc[4] == 'Hardware':
                if self.dvcHdwrCbck is None:
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Device Hardware callback (dvcHdwrCbck) required!")
                else:
                    self.dvcHdwrCbck(msg.topic, msg.payload)
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Device Hardware callback (dvcHdwrCbck) initiated!")
            elif stpc[4] == 'Notifications':
                if self.dvcNtfCbck is None:
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Device Notification callback (dvcNtfCbck) required!")
                else:
                    self.dvcNtfCbck(msg.topic, msg.payload)
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Device Notification callback (dvcNtfCbck) initiated!")
            elif stpc[4] == 'Warnings':
                if self.dvcWrnCbck is None:
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Device Warning callback (dvcWrnCbck) required!")
                else:
                    self.dvcWrnCbck(msg.topic, msg.payload)
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Device Warning callback (dvcWrnCbck) initiated!")
            elif stpc[4] == 'Sensors':
                if self.dvcSnsCbck is None:
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Device Sensor callback (dvcSnsCbck) required!")
                else:
                    self.dvcSnsCbck(msg.topic, msg.payload)
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Device Sensor callback (dvcHdwrCbck) initiated!")
            elif stpc[4] == 'Actuators':
                if self.dvcActCbck is None:
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Device Actuator callback (dvcActCbck) required!")
                else:
                    self.dvcActCbck(msg.topic, msg.payload)
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Device Actuator callback (dvcActCbck) initiated!")
            elif stpc[4] == 'Commands':
                if self.dvcCmmdCbck is None:
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Device Command callback (dvcCmmdCbck) required!")
                else:
                    self.dvcCmmdCbck(msg.topic, msg.payload)
                    self.Helpers.logMessage(self.LogFile, "JumpWayApp", "onMessage",
                                            "JumpWayMQTT JumpWayApp Device Command callback (dvcCmmdCbck) initiated!")
            elif stpc[4] == 'Camera':
                if self.cameraCallback is None:
                    print("** Device Camera Callback Required (cameraCallback)")
                else:
                    self.cameraCallback(msg.topic, msg.payload)

    def onLog(self, client, obj, level, string):

        print(string)

    def appDisconnect(self):
        self.appStsPub("OFFLINE")
        self.mqttClient.disconnect()
        self.mqttClient.loop_stop()
