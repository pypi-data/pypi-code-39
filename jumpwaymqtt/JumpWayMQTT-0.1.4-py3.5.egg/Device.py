############################################################################################
#
# Software:      iotJumpWay MQTT Python Clients
# Author:        Adam Milton-Barker (AdamMiltonBarker.com)
# License:       Eclipse Public License 2.0
#
# Title:         iotJumpWay MQTT Python JumpWayDvc Client
# Description:   An iotJumpWay MQTT Python JumpWayDvc Client that allows you to connect
#                to the iotJumpWay.
# Last Modified: 2019-04-07
#
############################################################################################

import os
import sys
import time
import json

import paho.mqtt.client as mqtt

from Classes.Helpers import Helpers


class JumpWayDvc():

    def __init__(self, params):
        """ inits the iotJumpWay JumpWayDvc class """

        self.parameters = params

        self.Helpers = Helpers()
        self.LogDir = os.getcwd() + "/Logs/Devices/"
        self.LogFile = self.Helpers.setLogFile(self.LogDir)

        self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "init",
                                "JumpWayMQTT JumpWayDvc logs initiated!")

        self.checkParameters()
        self.initCallbacks()
        self.initMQTT()

        self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "init",
                                "JumpWayMQTT JumpWayDvc initiated!")

    def checkParameters(self):
        """ Validates required incoming parameters """

        exitDvc = False
        msg = ""

        if self.parameters['JumpWayDvcLocID'] is None:
            msg = "JumpWayMQTT JumpWayDvc Location ID (JumpWayDvcLocID) parameter is required!"
            exitDvc = True
        elif self.parameters['JumpWayDvcZneID'] is None:
            msg = "JumpWayMQTT JumpWayDvc Zone ID (JumpWayDvcZneID) parameter is required!"
            exitDvc = True
        elif self.parameters['JumpWayDvcID'] is None:
            msg = "JumpWayMQTT JumpWayDvc ID (JumpWayDvcID) parameter is required!"
            exitDvc = True
        elif self.parameters['JumpWayDvcName'] is None:
            msg = "JumpWayMQTT JumpWayDvc name (JumpWayDvcName) parameter is required!"
            exitDvc = True
        elif self.parameters['username'] is None:
            msg = "JumpWayMQTT JumpWayDvc MQTT username (username) parameter is required!"
            exitDvc = True
        elif self.parameters['password'] is None:
            msg = "JumpWayMQTT JumpWayDvc MQTT password (password) parameter is required!"
            exitDvc = True

        if exitDvc is True:
            self.Helpers.logMessage(
                self.LogFile, "JumpWayDvc", "checkParameters", msg)
            sys.exit()
        else:
            self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "checkParameters",
                                    "JumpWayMQTT JumpWayDvc parameters OK!")

    def initMQTT(self):
        """ inits the iotJumpWay JumpWayDvc MQTT settings """

        self.mqttClient = None
        self.mqttTLS = os.path.dirname(
            os.path.abspath(__file__)) + "/CA/ca.pem"
        self.mqttHost = 'iot.techbubbletechnologies.com'
        self.mqttPort = 8883

    def initCallbacks(self):
        """ inits the iotJumpWay JumpWayDvc MQTT Callback functions """

        self.dvcStsCbck = None
        self.dvcHdwrCbck = None
        self.dvcNtfCbck = None
        self.dvcWrnCbck = None
        self.dvcSnsCbck = None
        self.dvcActCbck = None
        self.dvcCmmdCbck = None

        self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "initCallbacks",
                                "JumpWayMQTT JumpWayDvc MQTT Callbacks initiated!")

    def dvcCxn(self):
        """ inits an iotJumpWay JumpWayDvc MQTT connection """

        try:
            self.mqttClient = mqtt.Client(
                client_id=self.parameters['JumpWayDvcName'], clean_session=True)
            dvcStsTopic = '%s/Devices/%s/%s/Status' % (
                self.parameters['JumpWayDvcLocID'], self.parameters['JumpWayDvcZneID'], self.parameters['JumpWayDvcID'])
            self.mqttClient.will_set(dvcStsTopic, "OFFLINE", 0, False)
            self.mqttClient.tls_set(self.mqttTLS, certfile=None, keyfile=None)
            self.mqttClient.on_connect = self.onDvcCxn
            self.mqttClient.on_publish = self.onDvcPub
            self.mqttClient.on_subscribe = self.onDvcSub
            self.mqttClient.on_message = self.onDvcMessage
            self.mqttClient.username_pw_set(
                str(self.parameters['username']), str(self.parameters['password']))
            self.mqttClient.connect(self.mqttHost, self.mqttPort, 10)
            self.mqttClient.loop_start()
            time.sleep(4)

            self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "dvcCxn",
                                    "JumpWayMQTT JumpWayDvc MQTT Connection initiated!")
        except Exception as e:
            self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "dvcCxn",
                                    "JumpWayMQTT JumpWayDvc MQTT Connection initiation failed! " + str(e))
            exit()

    def onDvcCxn(self, client, obj, flags, rc):
        """ Triggered on successfull iotJumpWay JumpWayDvc MQTT connection """

        self.dvcStsPub("ONLINE")
        self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "onDvcCxn",
                                "JumpWayMQTT JumpWayDvc Connected successfully! RC: " + str(rc))

    def onDvcSub(self, client, obj, mid, granted_qos):
        """ Triggered on successfull iotJumpWay JumpWayDvc MQTT subscription """

        self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "onDvcSub",
                                "JumpWayMQTT JumpWayDvc subscribe: " + str(obj) + " " + str(mid) + " " + str(granted_qos))

    def dvcTpcSub(self, topicID, qos=0):
        """ Subscribes to an iotJumpWay JumpWayDvc MQTT topic """

        if self.parameters['JumpWayDvcLocID'] is None:
            self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "dvcTpcSub",
                                    "JumpWayMQTT JumpWayDvc Location ID (JumpWayDvcLocID) required!")
            return False
        elif self.parameters['JumpWayDvcZneID'] is None:
            self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "dvcTpcSub",
                                    "JumpWayMQTT JumpWayDvc Zone ID (JumpWayDvcZneID) required!")
            return False
        elif self.parameters['JumpWayDvcID'] is None:
            self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "dvcTpcSub",
                                    "JumpWayMQTT JumpWayDvc ID (JumpWayDvcID) required!")
            return False
        elif topicID is None:
            self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "dvcTpcSub",
                                    "JumpWayMQTT JumpWayDvc Topic ID (topicID) required!")
            return False
        else:
            dvcTpc = '%s/Devices/%s/%s/%s' % (self.parameters['JumpWayDvcLocID'],
                                              self.parameters['JumpWayDvcZneID'], self.parameters['JumpWayDvcID'], topicID)
            self.mqttClient.subscribe(dvcTpc, qos=qos)
            self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "dvcTpcSub",
                                    "JumpWayMQTT JumpWayDvc subscribed to JumpWayDvc " + str(self.parameters['JumpWayDvcID']) + " topic " + str(topicID) + "!")

    def onDvcPub(self, client, obj, mid):
        """ Triggered on successfull iotJumpWay JumpWayDvc MQTT publish """

        self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "onDvcPub",
                                "JumpWayMQTT JumpWayDvc publish: " + str(mid))

    def dvcStsPub(self, data):
        """ Publishes an iotJumpWay JumpWayDvc MQTT Status """

        if self.parameters['JumpWayDvcLocID'] is None:
            self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "dvcStsPub",
                                    "JumpWayMQTT JumpWayDvc Location ID (JumpWayDvcLocID) required!")
            return False
        elif self.parameters['JumpWayDvcZneID'] is None:
            self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "dvcStsPub",
                                    "JumpWayMQTT JumpWayDvc Zone ID (JumpWayDvcZneID) required!")
            return False
        elif self.parameters['JumpWayDvcID'] is None:
            self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "dvcStsPub",
                                    "JumpWayMQTT JumpWayDvc ID (JumpWayDvcID) required!")
            return False
        else:
            dvcStsTopic = '%s/Devices/%s/%s/Status' % (
                self.parameters['JumpWayDvcLocID'], self.parameters['JumpWayDvcZneID'], self.parameters['JumpWayDvcID'])
            self.mqttClient.publish(dvcStsTopic, data)
            self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "dvcStsPub",
                                    "JumpWayMQTT JumpWayDvc published to JumpWayDvc " + str(self.parameters['JumpWayDvcID']) + " topic Status!")
            return True

    def dvcTpcPub(self, topicID, data):

        if self.parameters['JumpWayDvcLocID'] is None:
            self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "dvcTpcPub",
                                    "JumpWayMQTT JumpWayDvc Location ID (JumpWayDvcLocID) required!")
            return False
        elif self.parameters['JumpWayDvcZneID'] is None:
            self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "dvcTpcPub",
                                    "JumpWayMQTT JumpWayDvc Zone ID (JumpWayDvcZneID) required!")
            return False
        elif self.parameters['JumpWayDvcID'] is None:
            self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "dvcTpcPub",
                                    "JumpWayMQTT JumpWayDvc ID (JumpWayDvcID) required!")
            return False
        elif topicID == None:
            self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "dvcTpcPub",
                                    "JumpWayMQTT JumpWayDvc Topic ID (JumpWayDvcID) required!")
            return False
        else:

            dvcTpc = '%s/Devices/%s/%s/%s' % (self.parameters['JumpWayDvcLocID'],
                                              self.parameters['JumpWayDvcZneID'], self.parameters['JumpWayDvcID'], topicID)
            self.mqttClient.publish(dvcTpc, json.dumps(data))
            self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "dvcTpcPub",
                                    "JumpWayMQTT JumpWayDvc published to JumpWayDvc " + str(self.parameters['JumpWayDvcID']) + " topic " + str(topicID) + "!")

    def onDvcMessage(self, client, obj, msg):
        """ Triggered on receiving iotJumpWay JumpWayDvc MQTT message """

        tpc = msg.topic
        stpc = tpc.split("/")

        self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "onMessage",
                                "JumpWayMQTT JumpWayDvc message received from " + tpc + " activity")

        if stpc[4] is 'Status':
            if self.dvcStsCbck is None:
                self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "onMessage",
                                        "JumpWayMQTT JumpWayDvc Device Status callback (dvcStsCbck) required!")
            else:
                self.dvcStsCbck(msg.topic, msg.payload)
                self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "onMessage",
                                        "JumpWayMQTT JumpWayDvc Device Status callback (dvcStsCbck) initiated!")
        elif stpc[4] == 'Hardware':
            if self.dvcHdwrCbck is None:
                self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "onMessage",
                                        "JumpWayMQTT JumpWayDvc Device Hardware callback (dvcHdwrCbck) required!")
            else:
                self.dvcHdwrCbck(msg.topic, msg.payload)
                self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "onMessage",
                                        "JumpWayMQTT JumpWayDvc Device Hardware callback (dvcHdwrCbck) initiated!")
        elif stpc[4] == 'Notifications':
            if self.dvcNtfCbck is None:
                self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "onMessage",
                                        "JumpWayMQTT JumpWayDvc Device Notification callback (dvcNtfCbck) required!")
            else:
                self.dvcNtfCbck(msg.topic, msg.payload)
                self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "onMessage",
                                        "JumpWayMQTT JumpWayDvc Device Notification callback (dvcNtfCbck) initiated!")
        elif stpc[4] == 'Warnings':
            if self.dvcWrnCbck is None:
                self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "onMessage",
                                        "JumpWayMQTT JumpWayDvc Device Warning callback (dvcWrnCbck) required!")
            else:
                self.dvcWrnCbck(msg.topic, msg.payload)
                self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "onMessage",
                                        "JumpWayMQTT JumpWayDvc Device Warning callback (dvcWrnCbck) initiated!")
        elif stpc[4] == 'Sensors':
            if self.dvcSnsCbck is None:
                self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "onMessage",
                                        "JumpWayMQTT JumpWayDvc Device Sensor callback (dvcSnsCbck) required!")
            else:
                self.dvcSnsCbck(msg.topic, msg.payload)
                self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "onMessage",
                                        "JumpWayMQTT JumpWayDvc Device Sensor callback (dvcHdwrCbck) initiated!")
        elif stpc[4] == 'Actuators':
            if self.dvcActCbck is None:
                self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "onMessage",
                                        "JumpWayMQTT JumpWayDvc Device Actuator callback (dvcActCbck) required!")
            else:
                self.dvcActCbck(msg.topic, msg.payload)
                self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "onMessage",
                                        "JumpWayMQTT JumpWayDvc Device Actuator callback (dvcActCbck) initiated!")
        elif stpc[4] == 'Commands':
            if self.dvcCmmdCbck is None:
                self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "onMessage",
                                        "JumpWayMQTT JumpWayDvc Device Command callback (dvcCmmdCbck) required!")
            else:
                self.dvcCmmdCbck(msg.topic, msg.payload)
                self.Helpers.logMessage(self.LogFile, "JumpWayDvc", "onMessage",
                                        "JumpWayMQTT JumpWayDvc Device Command callback (dvcCmmdCbck) initiated!")
        elif stpc[4] == 'Camera':
            if self.cameraCallback is None:
                print("** Device Camera Callback Required (cameraCallback)")
            else:
                self.cameraCallback(msg.topic, msg.payload)

    def onLog(self, client, obj, level, string):

        print(string)

    def dvcDisconnect(self):
        self.dvcStsPub("OFFLINE")
        self.mqttClient.disconnect()
        self.mqttClient.loop_stop()
