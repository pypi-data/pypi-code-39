#!/usr/bin/env python

import subprocess
import time
import os
from appium import webdriver
import random

class appium_server(object):
    random_port = random.randint(1111, 9999)
    random_bp = random.randint(11111,55555)

    def __init__(self,udid,app_path,adb_path,aapt_path):
        #配置基础参数
        self.aapt_path = aapt_path
        self.adb_path = adb_path
        self.app_path = app_path

        self.udid = udid
        cmd = "appium -a 127.0.0.1 -U %s -p %s -bp %s --command-timeout 100000 --session-override"%(udid,self.random_port,self.random_bp)
        subprocess.Popen(cmd,shell=True)
        time.sleep(5)

    def isAppium(self):
        # time.sleep(8)
        if os.name == "posix":
            pid = os.popen("lsof -i:%s|grep node|awk '{print $2}'"%str(self.random_port)).read()
        elif os.name == "nt":
            pid  = os.popen("netstat -ano|findStr 1125").read()[-8:].strip()

        if len(pid) != 0:
            return True
        return False



    def closeAppiumServer(self):
       if os.name == "posix":
            pid = os.popen("lsof -i:%s|grep node|awk '{print $2}'" % str(self.random_port)).read()
            return os.system("kill " + pid)
       elif os.name == "nt":
           netPort = os.popen("netstat -ano|findStr 1125").read()[-8:].strip()
           return os.system("taskkill /pid %s -t -f"%netPort)


    def driver_caps(self,isApp=False,isResetKeyboard=False):
        if os.name == "posix":
            aapt_dump = "%s dump badging %s |grep %s|awk '{print $2}'"
            appPackage = str(os.popen(aapt_dump % (self.aapt_path, self.app_path, "package")).read()).strip()[6:-1]
            appActivity = str(
                os.popen(aapt_dump % (self.aapt_path, self.app_path, "launchable-activity")).read()).strip()[6:-1]
        elif os.name == "nt":
            appActivity = os.popen(
                'aapt dump badging %s |findStr "launchable-activity"'%(self.app_path)).read().split(
                " ")[1].strip()[6:-1]
            appPackage = os.popen(
                'aapt dump badging  %s |findStr "package:" '%(self.app_path)).read().split(
                " ")[1].strip()[6:-1]


        # udids = str(os.popen("%s devices|grep -v devices|awk '{print $1}'" % (self.adb_path)).read()).split("\n")
        # udids = list(filter(None, udids))
        android_version = os.popen("%s shell getprop ro.build.version.release" % (self.adb_path)).read().strip()
        android_name = os.popen("%s shell getprop ro.product.name" % (self.adb_path)).read().strip()
        caps = {"platformName":"android",
            "platformVersion":android_version,
            "app":self.app_path,
            "udid":self.udid,
            "deviceName":android_name,
            "appPackage":appPackage,
            "appActivity":appActivity}
        if isResetKeyboard == True:
            caps.update({'unicodeKeyboard': True,
            'resetKeyboard': True})
        if isApp == True:
            caps.update({"noReset":True})

        return caps


    def startDriver(self,caps):
        # driver = webdriver.Remote('http://127.0.0.1:%s/wd/hub'%(self.random_port),caps)
        return webdriver.Remote('http://127.0.0.1:%s/wd/hub'%(self.random_port),caps)



if __name__ == '__main__':
    aapt_path = "/Library/android_sdk/build-tools/26.0.2/aapt"
    adb_path = "/Library/android_sdk/platform-tools/adb"
    app_path = "/Users/liaozhenghong/work/django-study/django-study/opencv/demo.apk"
    udid = "emulator-5554"
    appiumServer = appium_server(udid,app_path,adb_path,aapt_path)
    caps = appiumServer.driver_caps()
    appiumServer.startDriver(caps)
    time.sleep(5)
    print(appiumServer.closeAppiumServer())

