#!/usr/bin/env python
'''
一、环境配置

    1、Java环境
    2、adb环境
    3、appium服务
    4、Python3.7
    5、aapt环境配置


    详解：
    window 10
        1.1 java 环境
           安装：https://www.oracle.com/technetwork/java/javase/downloads/index.html
           变量配置教程：https://jingyan.baidu.com/article/6dad5075d1dc40a123e36ea3.html

        1.2 adb、aapt环境
           adb配置环境：https://jingyan.baidu.com/article/17bd8e52f514d985ab2bb800.html
           aapt环境配置：%Android_home%\build-tools\28.0.2\
           完整环境配置：
                1、新建Android_home，配置SDK的路径：C:\Users\LENOVO\AppData\Local\Android\Sdk
                2、配置adb、aapt环境：
                    %Android_home%\platform-tools\
                    %Android_home%\tools\
                    %Android_home%\build-tools\28.0.2\

        1.3 appium环境
            第一步:进入官网http://nodejs.cn/download/,安装node.
            第二步：安装完成node后，终端命令npm install -g appium
            第三步：配置appium环境变量（部分电脑路径可能会有所差异，根据实际进行配置）：
                \Users\LENOVO\AppData\Roaming\npm\node_modules\appium\node_modules\.bin
                \Users\LENOVO\AppData\Roaming\npm\node_modules\appium\node_module


    Macbook
        1.1  java环境配置
            安装：https://www.oracle.com/technetwork/java/javase/downloads/index.html
            变量配置教程：https://jingyan.baidu.com/article/6dad5075d1dc40a123e36ea3.html
            export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_191.jdk/Contents/Home
        1.2 adb、aapt环境配置
            export ANDROID_HOME=/Library/android_sdk
            export PATH=$PATH:$ANDROID_HOME/tools
            export PATH=$PATH:$ANDROID_HOME/platform-tools
            export JAVA_bin=".:$PATH:$JAVA_HOME/bin"
            export PATH=$PATH:$ANDROID_HOME/build-tools/26.0.2
            export PATH
        1.3 appium环境
            教程：https://www.jianshu.com/p/c48116494df7
'''
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
            pid  = os.popen("netstat -ano|findStr %s"%str(self.random_port)).read()[-8:].strip()

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

