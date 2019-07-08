#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

# Luis Enrique Coronado Zuniga

# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
import time
import os
import sys

class FaceTracking(ALModule):

    def __init__(self, name, ip):

        self.port = 9559
        self.ip = ip

        try: 
            self.name = name
            ALModule.__init__(self, name)
            proxy_name = "ALTracker"
            self.tracker = ALProxy( "ALTracker",self.ip, self.port)
            self.memory = ALProxy("ALMemory",self.ip, self.port)
            self.targetName = "People"
            self.distanceX = 0.0
            self.distanceY = 0.0
            self.angleWz = 0.0
            self.thresholdX = 0.0
            self.thresholdY = 0.0
            self.thresholdWz = 0.0
            self.effector = "None"
            self.subscribeDone = False
            self.isRunning = False
            self.memory.subscribeToEvent("ALTracker/ActiveTargetChanged", self.name, "onTargetChanged")
            print ( proxy_name + " success")
        except:
            print ( proxy_name + " error")

        
    def onUnload(self):
        if self.subscribeDone:
            self.memory.unsubscribeToEvent("ALTracker/TargetLost", self.name)
            self.memory.unsubscribeToEvent("ALTracker/TargetReached", self.name)
            self.subscribeDone = False

        if self.isRunning:
            self.tracker.setEffector("None")
            self.tracker.stopTracker()
            self.tracker.unregisterTarget(self.targetName)
            self.isRunning = False

    def onRun(self, input_ = "", parameters = {}, parallel = False):
        
        self.targetName = "People"      #  "Face"
        mode = "Move"                   # "WholeBody", "Move"
        self.distanceX = 0.3
        self.thresholdX = 0.1
        self.distanceY = 0.0
        self.thresholdY = 0.1
        self.angleWz = 0.0
        self.thresholdWz = 0.3
        self.effector = "None"          #  "None", "Arms", "LArms", "RArms"

        if self.subscribeDone:
            self.memory.unsubscribeToEvent("ALTracker/TargetLost", self.name)
            self.memory.unsubscribeToEvent("ALTracker/TargetReached", self.name)
            self.subscribeDone = False
        
        self.memory.subscribeToEvent("ALTracker/TargetLost", self.name, "onTargetLost")
        self.memory.subscribeToEvent("ALTracker/TargetReached", self.name, "onTargetReached")
        self.subscribeDone = True

        self.tracker.setEffector(self.effector)
        peopleIds = []
        self.tracker.registerTarget(self.targetName, peopleIds)
        self.tracker.setRelativePosition([-self.distanceX, self.distanceY, self.angleWz,
                                           self.thresholdX, self.thresholdY, self.thresholdWz])
        self.tracker.setMode(mode)

        self.tracker.track(self.targetName) # Start tracker
        self.isRunning = True

    def onStop(self):
        self.onUnload()

    def onTargetLost(self, key, value, message):
        print ("Target lost")
        #self.targetLost()

    def onTargetReached(self, key, value, message):
        print ("Target reached")
        #self.targetReached()

    def onTargetChanged(self, key, value, message):
        if value == self.targetName and not self.subscribeDone:
            self.memory.subscribeToEvent("ALTracker/TargetLost", self.name, "onTargetLost")
            self.memory.subscribeToEvent("ALTracker/TargetReached", self.name, "onTargetReached")
            self.subscribeDone = True
        elif value != self.targetName and self.subscribeDone:
            self.memory.unsubscribeToEvent("ALTracker/TargetLost", self.name)
            self.memory.unsubscribeToEvent("ALTracker/TargetReached", self.name)
            self.subscribeDone = False




robot_port = "9559"
robot_name = "pepper"
robot_ip = '192.168.0.100'
middleware = "nanomsg"
pattern = "survey"

pip   = robot_ip
pport = int(robot_port)

try:
    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       pip,         # parent broker IP
       pport)       # parent broker port


    SpeechEventListener = FaceTracking("FaceTrackingEventListener",pip)
    SpeechEventListener.onRun()
    
except Exception as e: 
    print(e)
    time.sleep(5)
    sys.exit(0)

try:
    while True:
        time.sleep(.1)
       
except KeyboardInterrupt:
    print
    print "Interrupted by user, shutting down"
    SpeechEventListener.onStop()
    myBroker.shutdown()
    sys.exit(0)

