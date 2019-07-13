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

# Template action funtion:
"""

class name:
    def __init__(self,ip,port=9559):
        self.ip = ip
        self.port = port

    def onLoad(self):
        try: 
            proxy_name "AL.."
            self.proxy = ALProxy(proxy_name, self.ip, self.port)
            print ( proxy_name + " success")
        except:
            print ( proxy_name + " error")

    #onRun for action, onInput for peception.
    def onRun(self, input_ = "", parameters = {}, parallel = "false"):   

    def onStop(self, input_ = "", parameters = {}, parallel = "false"):


"""
# Template module:
"""

class NameModule(ALModule):
    def __init__(self, name, robot, ip  port = 9559):
        ALModule.__init__(self, name)
        self.name = name
        self.robot = robot
        self.ip = ip
        self.port = port
        try: 
            proxy_name = "AL.."
            self.proxy = ALProxy(proxy_name,self.ip,self.port)
            self.memory = ALProxy("ALMemory",self.ip, self.port)
            print ( proxy_name + " success")

            try:
                self.memory.subscribeToEvent(EventName, self.name, "EventListener")
            except():
                self.memory.unsubscribeToEvent(EventName, self.name)
                self.memory.subscribeToEvent(EventName, self.name, "EventListener")

        except:
            print ( proxy_name + " error")

    def EventListener(self, key, value, message):


"""


class Sonars:
    def __init__(self, memory, sharo, robot):
        self.memoryProxy = memory
        self.robot = robot
        self.sharo = sharo
        self.run = True
    
    def onRun(self):
        
        old_proximity = "none"
        proximity = "none"
        error = False

       

        while self.run:

            try:
                front_value = memoryProxy.getData("Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value")
                back_value = memoryProxy.getData("Device/SubDeviceList/Platform/Back/Sonar/Sensor/Value")


                if front_value < 0.5:
                        proximity = "close"
                elif front_value < 1 and front_value > 0.5:
                        proximity = "middle"
                elif front_value < 1.5:
                    proximity = "far"
               
                if not old_proximity == proximity:

                    print "human " + proximity
                    if proximity == "close":
                        data = {"node":"perception", "primitive":"human_distance", "input":"add", "robot":self.robot, "parameters":{proximity:1}}
                    elif proximity == "middle":
                         data = {"node":"perception", "primitive":"human_distance", "input":"add", "robot":self.robot, "parameters":{proximity:1}}
                    else:
                         data = {"node":"perception", "primitive":"human_distance", "input":"add", "robot":self.robot, "parameters":{proximity:1}}
                    sharo.send_json(data)

                old_proximity = proximity
            except:
                if not error:
                    print ("Sonar problem")
                    error = True
                else:
                    pass
            time.sleep(.01)