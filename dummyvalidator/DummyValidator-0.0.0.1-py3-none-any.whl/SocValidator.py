# SocValidator.py
# copyright 2019, Microsoft

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time, datetime
import sys, os, glob, shutil

import threading
from threading import Thread, Lock
import socket

import csv, re, xml.etree.ElementTree as ET
from collections import OrderedDict
import clipboard

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QWidget, QVBoxLayout
from PyQt5.QtWidgets import QTabWidget, QPushButton, QFileDialog
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import serial  # note, this is "PySerial" package
import serial.tools.list_ports

import nidaqmx

from xbconnect import xbconnect
from Console import RunXBApps
from VReg import Vregscontrol

qtCreatorFile = "SocValidatorGUI.ui"  # UI file from QtDesigner
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
appIsEnding = False

class GuiComm(QtCore.QObject):  # (pyqtSignal requires this to be in a class)
    signalProgressAuto = QtCore.pyqtSignal(int)
    signalProgressSampling = QtCore.pyqtSignal(int)
    signalPackageTemp = QtCore.pyqtSignal(str)
    signalPackageTempTarget = QtCore.pyqtSignal(float)
    signalDieTemp = QtCore.pyqtSignal(str)
    signalClearDieTempAutoAdjust = QtCore.pyqtSignal()
    signalClearStatus = QtCore.pyqtSignal()
    signalClearKdhost = QtCore.pyqtSignal()
    signalClearKdsra = QtCore.pyqtSignal()
    signalClearKdera = QtCore.pyqtSignal()
    signalClearDsmc = QtCore.pyqtSignal()
    signalAppendStatus = QtCore.pyqtSignal(str)
    signalAppendKdhost = QtCore.pyqtSignal(str)
    signalAppendKdsra = QtCore.pyqtSignal(str)
    signalAppendKdera = QtCore.pyqtSignal(str)
    signalAppendDsmc = QtCore.pyqtSignal(str)
    signalSetKdhostErrorColor = QtCore.pyqtSignal(bool)
    signalSetKdsraErrorColor = QtCore.pyqtSignal(bool)
    signalSetKderaErrorColor = QtCore.pyqtSignal(bool)
    signalUpdateVipAndPlot = QtCore.pyqtSignal(list)
    signalUpdateScreenshot = QtCore.pyqtSignal()

class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.axes = [None, None, None]
        self.lockMode = Lock()
        self.mode = None  # note three-state, eg 'V'/'I'/..../'VIP'
        #
        self.layoutVertical = QVBoxLayout(self)
        self.layoutVertical.addWidget(self.canvas)
        #
        self.lockBuffer = Lock()
        self.plotBuffer = [[[] for i in range(9)] for j in range(3)]  # 3 plots, each have 9 lists
        self.maxBufferSize = 100
    def SetMode(self, mode):
        if self.mode==mode:
            return
        with self.lockMode:
            self.mode = mode
            numPlots = len(self.mode)
            if (numPlots>0)and(numPlots<=3):
                # clear existing
                for i in range(3):
                    if self.axes[i]!=None:
                        self.figure.delaxes(self.axes[i])
                        self.axes[i] = None
                #
                if numPlots==1:  # one plot: 111
                    if mode=='V':
                        self.axes[0] = self.figure.add_subplot(111)
                        self.axes[0].clear()
                    elif mode=='I':
                        self.axes[1] = self.figure.add_subplot(111)
                        self.axes[1].clear()
                    elif mode=='P':
                        self.axes[2] = self.figure.add_subplot(111)
                        self.axes[2].clear()
                    else:
                        pass  # should not get here
                elif numPlots==2:  # two plots: 121/122
                    if mode=='VI':
                        self.axes[0] = self.figure.add_subplot(121) 
                        self.axes[0].clear()
                        self.axes[1] = self.figure.add_subplot(122)
                        self.axes[1].clear()
                    elif mode=='VP':
                        self.axes[0] = self.figure.add_subplot(121) 
                        self.axes[0].clear()
                        self.axes[2] = self.figure.add_subplot(122)
                        self.axes[2].clear()
                    elif mode=='IP':
                        self.axes[1] = self.figure.add_subplot(121) 
                        self.axes[1].clear()
                        self.axes[2] = self.figure.add_subplot(122)
                        self.axes[2].clear()
                    else:
                        pass  # should not get here
                elif numPlots==3:  # three plots: 131/132/133
                    for plotIndex in range(numPlots):
                        self.axes[plotIndex] = self.figure.add_subplot(131+plotIndex)
                        self.axes[plotIndex].clear()
                else:
                    pass  # should not get here
        self.DoPlottingAndCanvasDraw()
    def DoPlottingAndCanvasDraw(self):
        try:
            with self.lockBuffer:
                for plotIndex in range(3):
                    if self.axes[plotIndex]==None:
                        continue
                    self.axes[plotIndex].clear()
                    #
                    for setIndex in range(9):
                        plotBuffer = self.plotBuffer[plotIndex][setIndex]
                        lenPlotBuffer = len(plotBuffer)
                        if lenPlotBuffer==0:
                            self.axes[plotIndex].set_xticks(range(0,1,1))
                        elif lenPlotBuffer<=10:
                            self.axes[plotIndex].set_xticks(range(0,lenPlotBuffer,1))
                        elif lenPlotBuffer<=20:
                            self.axes[plotIndex].set_xticks(range(0,lenPlotBuffer,5))
                        elif lenPlotBuffer<=50:
                            self.axes[plotIndex].set_xticks(range(0,lenPlotBuffer,10))
                        elif lenPlotBuffer<=80:
                            self.axes[plotIndex].set_xticks(range(0,lenPlotBuffer,20))
                        else:
                            self.axes[plotIndex].set_xticks(range(0,lenPlotBuffer,20))
                        #
                        self.axes[plotIndex].plot(plotBuffer)
        except:
            pass
        # customize
        for plotIndex in range(3):
            if self.axes[plotIndex]==None:
                continue
            if plotIndex==0:
                self.axes[0].set_ylabel('Voltage (V)', fontsize='6')
            elif plotIndex==1:
                self.axes[1].set_ylabel('Current (A)', fontsize='6')
            elif plotIndex==2:
                self.axes[2].set_ylabel('Power (W)', fontsize='6')
            self.axes[plotIndex].set_xlabel('Samples', fontsize='6')
            self.axes[plotIndex].xaxis.set_tick_params(labelsize=6)
            self.axes[plotIndex].yaxis.set_tick_params(labelsize=6)
        self.figure.tight_layout()
        #
        self.canvas.draw()
    def AddPlotData(self, packPlot):
        # packPlot = [dataV, dataI, dataP]
        try:
            with self.lockBuffer:
                for plotIndex in range(3):
                    for setIndex in range(9):
                        plotBuffer = self.plotBuffer[plotIndex][setIndex]
                        value = packPlot[plotIndex][setIndex]
                        if value==None:
                            continue
                        plotBuffer.append(value)
                        if len(plotBuffer)>self.maxBufferSize:
                            plotBuffer.pop(0)
                        self.plotBuffer[plotIndex][setIndex] = plotBuffer
        except:
            pass
    def ClearPlotData(self):
        try:
            with self.lockBuffer:
                self.plotBuffer = [[[] for i in range(9)] for j in range(3)]
        except:
            pass
    def SetFrameGeometry(self, fg):
        try:
            super().resize(fg.width(), fg.height())
            super().move(fg.x(), fg.y())
        except:
            return False
        return True

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setFixedSize(self.size())

        # GUI communications
        self.threadIntervalInSeconds = 0.500
        self.threadIntervalInSecondsWhenBusy = 0.100
        self.timeBetweenTempUpdatesInSeconds = 2.000
        self.timeBetweenTempAdjustsInSeconds = 5.000
        self.timeBetweenScreenshotUpdatesInSeconds = 3.000
        self.guicomm = GuiComm()
        self.guicomm.signalProgressAuto.connect(self.UpdateProgressAuto)
        self.guicomm.signalProgressSampling.connect(self.UpdateProgressSampling)
        self.guicomm.signalPackageTemp.connect(self.UpdatePackageTemp)
        self.guicomm.signalPackageTempTarget.connect(self.UpdatePackageTempTarget)
        self.guicomm.signalDieTemp.connect(self.UpdateDieTemp)
        self.guicomm.signalClearDieTempAutoAdjust.connect(self.ClearDieTempAutoAdjust)
        self.guicomm.signalClearStatus.connect(self.ClearStatus)
        self.guicomm.signalClearKdhost.connect(self.ClearKdhost)
        self.guicomm.signalClearKdsra.connect(self.ClearKdsra)
        self.guicomm.signalClearKdera.connect(self.ClearKdera)
        self.guicomm.signalClearDsmc.connect(self.ClearDsmc)
        self.guicomm.signalAppendStatus.connect(self.AppendStatus)
        self.guicomm.signalAppendKdhost.connect(self.AppendKdhost)
        self.guicomm.signalAppendKdsra.connect(self.AppendKdsra)
        self.guicomm.signalAppendKdera.connect(self.AppendKdera)
        self.guicomm.signalAppendDsmc.connect(self.AppendDsmc)
        self.guicomm.signalUpdateVipAndPlot.connect(self.UpdateVipAndPlot)
        self.guicomm.signalSetKdhostErrorColor.connect(self.SetKdhostErrorColor)
        self.guicomm.signalSetKdsraErrorColor.connect(self.SetKdsraErrorColor)
        self.guicomm.signalSetKderaErrorColor.connect(self.SetKderaErrorColor)
        self.guicomm.signalUpdateScreenshot.connect(self.UpdateScreenshot)

        # TEC and Diode
        self.btnSetPackageTemp.clicked.connect(self.SetPackageTemp)
        self.btnSetDieTemp.clicked.connect(self.SetDieTemp)
        self.chkDieTempAutoAdjust.stateChanged.connect(self.DieTempAutoAdjustChanged)
        self.chkDieTempStopWhenStable.stateChanged.connect(self.DieTempStopWhenStableChanged)
        # Screenshot
        self.doScreenshotUpdate = False
        self.btnScreenshot.clicked.connect(self.ScreenshotOnOffChanged)
        # main Tab
        self.tabMain.currentChanged.connect(self.TabMainChange)
        # Manual tab, Rails
        self.PopulateRailsBoardTypes()
        self.btnRailsSet.clicked.connect(self.RailsSet)
        self.btnRailsGet.clicked.connect(self.RailsGet)
        self.btnRailsSet.setEnabled(False)  # disabled until discovery is done then enable
        self.btnRailsGet.setEnabled(False)  # disabled until discovery is done then enable
        # Manual tab, TEC
        self.btnTecComPortUpdate.clicked.connect(self.TecComPortUpdate)
        self.tec = SerialTec()
        self.tec.Setup(useThisPort=None)
        if not self.tec.IsValid():
            self.textStatus.append('Error: Did not initialize TEC properly!!')
        else:
            self.lineTecComPort.setText(self.tec.ser.port)
            self.textStatus.append('Initialized TEC properly (' + self.tec.ser.port + ').')
        # Manual tab, AMD HDT Debugger
        self.btnDebuggerIpUpdate.clicked.connect(self.DebuggerIpUpdate)
        # Manual tab, Xbox Console
        self.xboxStateMachine = XboxStateMachine()
        self.xboxStateMachine.DeleteLogFiles()
        #
        self.btnConsoleDiscover.clicked.connect(self.ConsoleDiscover)
        self.btnConsolePingHost.clicked.connect(self.ConsolePingHost)
        self.btnConsolePingSystem.clicked.connect(self.ConsolePingSystem)
        self.btnConsoleCommandSend.clicked.connect(self.ConsoleCommandSend)
        self.PopulateConsoleActions()
        self.comboConsoleAction.currentTextChanged.connect(self.ConsoleActionChanged)
        self.EnableDiscoveryUI(discoveryGood=False, allowDiscovery=True)
        #
        self.PopulateDeployApps()  # note, will call PopulateLaunchTerminateApps()
        self.btnAppDeploy.clicked.connect(self.AppDeploy)
        self.btnAppDeployAll.clicked.connect(self.AppDeployAll)
        self.btnAppLaunch.clicked.connect(self.AppLaunch)
        self.btnAppTerminate.clicked.connect(self.AppTerminate)
        # Manual tab, Display Resolution
        self.PopulateResolutions()
        self.btnResolutionUpdate.clicked.connect(self.ResolutionUpdate)

        # Automation tab
        self.PopulateAutoRailsBoardTypes()
        self.btnAutoConfigFileBrowse.clicked.connect(self.AutoConfigFileBrowse)
        self.btnAutoConfigFileLoad.clicked.connect(self.AutoConfigFileLoad)
        self.btnAutoFileBrowse.clicked.connect(self.AutoFileBrowse)
        self.btnAutoFileLoad.clicked.connect(self.AutoFileLoad)
        self.btnAutoGo.clicked.connect(self.AutoGo)
        self.btnAutoStop.clicked.connect(self.AutoStop)

        # NI DAQ tab
        self.nidaqHandler = NidaqHandler()
        self.nidaqHandler.SetupPoolThreads()
        self.btnSamplingConfigFileBrowse.clicked.connect(self.SamplingConfigFileBrowse)
        self.btnSamplingConfigFileLoad.clicked.connect(self.SamplingConfigFileLoad)
        self.btnSamplingOneSample.clicked.connect(self.SamplingOneSample)
        self.btnSamplingLive.clicked.connect(self.SamplingLive)
        self.btnSamplingGo.clicked.connect(self.SamplingGo)
        self.btnSamplingStop.clicked.connect(self.SamplingStop)
        self.chkSamplingOverride.stateChanged.connect(self.SamplingOverrideChanged)
        self.btnSamplingClipboard.clicked.connect(self.SamplingClipboard)
        self.PopulateSamplingFrame()
        self.comboSamplingFrame.currentTextChanged.connect( \
            self.SamplingFrameChanged)
        self.PopulateSamplingPlotOptions()
        self.comboSamplingPlotOptions.currentTextChanged.connect( \
            self.SamplingPlotOptionsChanged)
        self.SamplingOverrideChanged(QtCore.Qt.Unchecked)
        self.btnSamplingReset.clicked.connect(self.SamplingReset)
        self.btnSamplingFreeze.clicked.connect(self.SamplingFreeze)
        self.EnableSamplingUI(allowSampling=True)
        #
        self.labelPlot1.setStyleSheet('color: blue')
        self.labelPlot2.setStyleSheet('color: orange')
        self.labelPlot3.setStyleSheet('color: green')
        self.labelPlot4.setStyleSheet('color: red')
        self.labelPlot5.setStyleSheet('color: purple')
        self.labelPlot6.setStyleSheet('color: brown')
        self.labelPlot7.setStyleSheet('color: pink')
        self.labelPlot8.setStyleSheet('color: gray')
        self.labelPlot9.setStyleSheet('color: olive')
        #
        self.visualFreeze = False
        self.visualFreezePack = []
        # Plot
        self.plotSampling = MatplotlibWidget(parent=self.groupSampling)
        self.SamplingPlotOptionsChanged(value='No Plots')
        # Automation state machine
        self.appIsEnding = False
        self.stateAutoRunning = False
        self.stateSamplingRunning = False
        self.btnAutoGo.setEnabled(True)
        self.btnAutoStop.setEnabled(False)
        # note, infoTemp is
        #   [tecTarget, dieTarget, tecActual, dieActual, tecReadFails, dieReadFails]
        self.infoTemp = [None, None, None, None, 0, 0]
        # note, infoTempAutoAdjust is
        #   [autoAdjust, stopWhenStable, stopWhenStableCounter]
        self.infoTempAutoAdjust = [None, None, 0]
        self.tempAdjustRange = 0.5  # adjusting amount threshold needed to bother adjusting TEC
        self.tempStableRange = 1.0  # adjusting amount threshold needed to be considered stable
        self.tempStableCountNeeded = 10  # temperature considered stable after this many count
        self.DieTempAutoAdjustChanged(QtCore.Qt.Unchecked)  # sets infoTempAutoAdjust[0]
        self.DieTempStopWhenStableChanged(QtCore.Qt.Unchecked)  # sets infoTempAutoAdjust[1]
        #
        self.thread = Thread(target=self.GuiBackgroundThread)
        self.thread.start()

    @QtCore.pyqtSlot(int)
    def UpdateProgressAuto(self, value):
        self.progAuto.setValue(value)
    @QtCore.pyqtSlot(int)
    def UpdateProgressSampling(self, value):
        self.progSamplingOutput.setValue(value)
    @QtCore.pyqtSlot(str)
    def UpdatePackageTemp(self, value):
        try:
            self.lineActualPackageTemp.setText(value)
        except:
            pass
    @QtCore.pyqtSlot(float)
    def UpdatePackageTempTarget(self, value):
        try:
            self.spinPackageTemp.setValue(value)
        except:
            pass
    @QtCore.pyqtSlot(str)
    def UpdateDieTemp(self, value):
        self.lineActualDieTemp.setText(value)
    @QtCore.pyqtSlot()
    def ClearDieTempAutoAdjust(self):
        self.chkDieTempAutoAdjust.setChecked(False)
    @QtCore.pyqtSlot()
    def ClearStatus(self):
        self.textStatus.clear()
    @QtCore.pyqtSlot()
    def ClearKdhost(self):
        self.textKdhost.clear()
    @QtCore.pyqtSlot()
    def ClearKdsra(self):
        self.textKdsra.clear()
    @QtCore.pyqtSlot()
    def ClearKdera(self):
        self.textKdera.clear()
    @QtCore.pyqtSlot()
    def ClearDsmc(self):
        self.textDsmc.clear()
    @QtCore.pyqtSlot(str)
    def AppendStatus(self, value):
        self.textStatus.append(value)
    @QtCore.pyqtSlot(str)
    def AppendKdhost(self, value):
        self.textKdhost.append(value)
    @QtCore.pyqtSlot(str)
    def AppendKdsra(self, value):
        self.textKdsra.append(value)
    @QtCore.pyqtSlot(str)
    def AppendKdera(self, value):
        self.textKdera.append(value)
    @QtCore.pyqtSlot(str)
    def AppendDsmc(self, value):
        self.textDsmc.append(value)
    @QtCore.pyqtSlot(list)
    def UpdateVipAndPlot(self, packVipAndPlot):
        try:
            packVip, packPlot = packVipAndPlot
            #
            rowCount = self.tableSampling.rowCount() - 1  # -1 due to 'Plot?' row
            colCount = self.tableSampling.columnCount()
            for row in range(rowCount):  # should be 3: ['V', 'I', 'P']
                for col in range(colCount):
                    value = packVip[row+1][col]  # +1 due to header
                    if value!=None:
                        value = '{0}'.format(float("{0:.3g}".format(value)))
                    else:
                        value = ''
                    self.tableSampling.setItem(row, col, QTableWidgetItem(value))
            totalPower = packVip[4][0]
            if totalPower!=None:
                self.lineSamplingTotalPower.setText('{0}'.format(float("{0:.3g}".format(totalPower))))
            else:
                self.lineSamplingTotalPower.setText('')
            # plot
            self.plotSampling.AddPlotData(packPlot)
            self.plotSampling.DoPlottingAndCanvasDraw()
        except:
            pass
    @QtCore.pyqtSlot(bool)
    def SetKdhostErrorColor(self, value):
        self.SetKdErrorColorHelper(1, value)
    @QtCore.pyqtSlot(bool)
    def SetKdsraErrorColor(self, value):
        self.SetKdErrorColorHelper(2, value)
    @QtCore.pyqtSlot(bool)
    def SetKderaErrorColor(self, value):
        self.SetKdErrorColorHelper(3, value)
    def SetKdErrorColorHelper(self, tabIndex, value):
        try:
            if value:
                self.tabStatus.tabBar().setTabTextColor(tabIndex, QtCore.Qt.red)
            else:
                self.tabStatus.tabBar().setTabTextColor(tabIndex, QtCore.Qt.green)
        except:
            pass
    @QtCore.pyqtSlot()
    def UpdateScreenshot(self):
        # show actual screenshot, if not possible then just show logo
        filename = '.\\XboxScreenshot.png'
        qsize = QtCore.QSize(200, 100)
        if not os.path.exists(filename):
            filename = '.\\XboxLogo.png'
            qsize = QtCore.QSize(161, 71)
        try:
            self.btnScreenshot.setIcon(QtGui.QIcon(filename))
            self.btnScreenshot.setIconSize(qsize)
        except:
            pass

    def closeEvent(self, event):
        self.appIsEnding = True
        self.nidaqHandler.PoolCleanup()
        self.xboxStateMachine.KillLogProcesses()
        time.sleep(1)
    def GuiBackgroundThread(self):
        nextTempUpdateDatetime = datetime.datetime.now()
        deltaTempUpdateDatetime = datetime.timedelta( \
            microseconds=self.timeBetweenTempUpdatesInSeconds*1000000)
        nextTempAdjustDatetime = datetime.datetime.now()
        deltaTempAdjustDatetime = datetime.timedelta( \
            microseconds=self.timeBetweenTempAdjustsInSeconds*1000000)
        nextScreenshotUpdateDatetime = datetime.datetime.now()
        deltaScreenshotUpdateDatetime = datetime.timedelta( \
            microseconds=self.timeBetweenScreenshotUpdatesInSeconds*1000000)
        # infoTemp: [tecTarget, dieTarget, tecActual, dieActual, tecReadFails, dieReadFails]
        while not self.appIsEnding:
            nowDatetime = datetime.datetime.now()
            if nowDatetime>nextTempUpdateDatetime:
                nextTempUpdateDatetime = nowDatetime + deltaTempUpdateDatetime
                self.tec.AskTemp()
                # Diode, reset fail counter as needed
                self.infoTemp[3] = xbconnect.ReadMaxDiodeTemp()
                if self.infoTemp[3]!=None:
                    tempActual = '{0:.1f}'.format(self.infoTemp[3])
                    self.guicomm.signalDieTemp.emit(tempActual)
                    self.infoTemp[5] = 0
                else:
                    self.infoTemp[5] += 1
                    if self.infoTemp[5]>5:
                        self.guicomm.signalDieTemp.emit('NA')
                # TEC, reset fail counter as needed
                self.infoTemp[2] = self.tec.ReceiveTemp()
                if self.infoTemp[2]!=None:
                    tempActual = '{0:.1f}'.format(self.infoTemp[2])
                    self.guicomm.signalPackageTemp.emit(tempActual)
                    self.infoTemp[4] = 0
                else:
                    self.infoTemp[4] += 1
                    if self.infoTemp[4]>5:
                        self.guicomm.signalPackageTemp.emit('NA')
            # note, following logic is replicated in utoSetupNextTest/AutoWaitForTempDone
            if (self.infoTempAutoAdjust[0])and(nowDatetime>nextTempAdjustDatetime):
                nextTempAdjustDatetime = nowDatetime + deltaTempAdjustDatetime
                tecTarget, dieTarget, tecActual, dieActual, \
                    tecReadFails, dieReadFails = self.infoTemp
                if (tecActual!=None)and(dieTarget!=None)and(dieActual!=None):
                    adjustTec = (dieTarget-dieActual)/2.0
                    if adjustTec>0:
                        adjustTec = min(adjustTec, 10.0)
                    else:
                        adjustTec = max(adjustTec, -10.0)
                    if tecTarget==None:  # if tecTarget never set, assume same as actual
                        tecTarget = tecActual
                    # only adjust TEC if big enough to bother adjusting TEC
                    if (adjustTec<-self.tempAdjustRange)or(adjustTec>self.tempAdjustRange):
                        tecTarget += adjustTec
                        tecTarget = min(max(tecTarget, 15.0), 100.0)  # sanity
                        tecTarget = round(tecTarget, 1)  # must round to 1 digit to match TEC display
                        self.infoTemp[0] = tecTarget
                        #
                        self.guicomm.signalPackageTempTarget.emit(tecTarget)
                        self.tec.SetTemp(tecTarget)
                    # if need to stop AutoAdjust: check if stable, using counter
                    if self.infoTempAutoAdjust[1]:
                        if (adjustTec<self.tempStableRange)and(adjustTec>-self.tempStableRange):
                            self.infoTempAutoAdjust[2] += 1
                            if self.infoTempAutoAdjust[2]>self.tempStableCountNeeded:
                                self.guicomm.signalClearDieTempAutoAdjust.emit()
                                self.infoTempAutoAdjust[0] = False
                                self.infoTempAutoAdjust[2] = 0
                        else:
                            self.infoTempAutoAdjust[2] = 0
            #
            if self.doScreenshotUpdate and (nowDatetime>nextScreenshotUpdateDatetime):
                try:
                    os.remove('.\\XboxScreenshot.png')
                except:
                    pass
                #
                hostip = xbconnect.GetConsoleHostIP()
                xbconnect.CaptureScreenshot(hostip)
                self.guicomm.signalUpdateScreenshot.emit()
                nextScreenshotUpdateDatetime = nowDatetime + deltaScreenshotUpdateDatetime
            #
            if self.stateSamplingRunning:
                if self.nidaqHandler.IsSamplingAndFlushingDone():
                    self.stateSamplingRunning = False
                    self.EnableSamplingUI(allowSampling=True)
                    self.EnableAutomationUI(allowRunning=True)
                    self.textStatus.append('Finished running Sampling test...')
                    self.guicomm.signalProgressSampling.emit(100)
                elif self.nidaqHandler.killStatus:
                    self.nidaqHandler.FlushSamplesHeld(cbProgress=self.FlushProgressCallback, \
                        cbVipAndPlot=self.UpdateVipAndPlotCallback)
                    self.stateSamplingRunning = False
                    self.EnableSamplingUI(allowSampling=True)
                    self.EnableAutomationUI(allowRunning=True)
                    self.textStatus.append('Stopped Sampling test.')
                    self.nidaqHandler.killStatus = False
                else:
                    self.nidaqHandler.FlushSamplesHeld( \
                        cbProgress=self.FlushProgressCallback, \
                        cbVipAndPlot=self.UpdateVipAndPlotCallback)
            elif self.stateAutoRunning:
                self.xboxStateMachine.OnTick()
                isDiscoveryDone = self.xboxStateMachine.IsDiscoveryDone()
                isAutoDone = self.xboxStateMachine.IsAutoDone()
                if isDiscoveryDone or isAutoDone:
                    # update GUI with Xbox Host IP, System IP, etc
                    if self.xboxStateMachine.HasErrors():
                        self.xboxStateMachine.ClearErrors()
                        self.EnableSamplingUI(allowSampling=True)
                        self.EnableDiscoveryUI(discoveryGood=False, allowDiscovery=True)
                        self.EnableAutomationUI(allowRunning=True)
                        self.lineConsoleHostIP.setText('')
                        self.lineConsoleSystemIP.setText('')
                        self.textStatus.append('Failed to do Xbox Discovery!!')
                    else:
                        discoveryResult = self.xboxStateMachine.GetDiscoveryResults()
                        # (ConsoleHostIP, ConsoleSystemIP, kdhostPid, kdsraPid, kderaPid)
                        self.lineConsoleHostIP.setText(discoveryResult[0])
                        self.lineConsoleSystemIP.setText(discoveryResult[1])
                        self.EnableSamplingUI(allowSampling=True)
                        self.EnableDiscoveryUI(discoveryGood=True, allowDiscovery=True)
                        self.EnableAutomationUI(allowRunning=True)
                    self.xboxStateMachine.ClearDiscoveryDone()
                    self.stateAutoRunning = False
                if isAutoDone:
                    self.btnAutoGo.setEnabled(True)
                    self.btnAutoStop.setEnabled(False)
                    self.btnAutoConfigFileBrowse.setEnabled(True)
                    self.btnAutoConfigFileLoad.setEnabled(True)
                    self.btnAutoFileBrowse.setEnabled(True)
                    self.btnAutoFileLoad.setEnabled(True)
                    self.xboxStateMachine.ClearAutoDone()
            if self.stateSamplingRunning or self.stateAutoRunning:
                time.sleep(self.threadIntervalInSecondsWhenBusy)
            else:
                time.sleep(self.threadIntervalInSeconds)
            self.xboxStateMachine.ShowLogsAndCheckForKnownError(guicomm=self.guicomm)
        return
    def FlushProgressCallback(self, progress):
        try:
            self.guicomm.signalProgressSampling.emit(progress)
        except:
            pass
    def UpdateVipAndPlotCallback(self, packVipAndPlot):
        try:
            if not self.visualFreeze:
                self.guicomm.signalUpdateVipAndPlot.emit(packVipAndPlot)
        except:
            pass

    # NI Daq Sampling
    def EnableSamplingUI(self, allowSampling, enableStopButton=None):
        self.btnSamplingOneSample.setEnabled(allowSampling)
        self.btnSamplingLive.setEnabled(allowSampling)
        self.btnSamplingGo.setEnabled(allowSampling)
        if enableStopButton!=None:
            self.btnSamplingStop.setEnabled(enableStopButton)
        else:
            self.btnSamplingStop.setEnabled(not allowSampling)
        self.btnSamplingConfigFileBrowse.setEnabled(allowSampling)
        self.btnSamplingConfigFileLoad.setEnabled(allowSampling)
    def SamplingConfigFileBrowse(self):
        filename = self.lineSamplingConfigFile.text()
        try:
            filespec = QFileDialog.getOpenFileName(self, \
                filename, './', 'PJDaq Files(*.PJDaq)')
            if filespec[0]=='':
                filespec[0] = filename
            self.lineSamplingConfigFile.setText(filespec[0])
        except:
            pass
    def SamplingConfigFileLoad(self):
        configFilename = self.lineSamplingConfigFile.text()
        if not self.nidaqHandler.ParseNidaqXml(filename=configFilename):
            self.textStatus.append('Failed to load configuration/XML file (' + configFilename + ')!!')
        else:
            packPlotVars = [self.labelPlot1, self.labelPlot2, self.labelPlot3, \
                self.labelPlot4, self.labelPlot5, self.labelPlot6, \
                self.labelPlot7, self.labelPlot8, self.labelPlot9]
            self.nidaqHandler.PopulateSamplingTable(
                tableSampling=self.tableSampling, packPlotVars=packPlotVars)
            self.lineSampleRate.setText(str(self.nidaqHandler.sampleRate))
            self.lineSampleOversample.setText(str(self.nidaqHandler.sampleOversample))
            self.lineSampleCount.setText(str(self.nidaqHandler.sampleCountMax))
            self.textStatus.append('Successfully loaded configuration/XML file (' + configFilename + ').')
    def BuildOverrideParams(self):
        if not self.chkSamplingOverride.isChecked():
            return None
        orParams = [None, None, None]  # [sampleRate, sampleOversample, sampleCountMax]
        try:
            # sanity
            value = int(self.lineSampleRate.text())
            orParams[0] = min(100000, max(1000, value))
            # use an oversample value that can divide into 500
            value = int(self.lineSampleOversample.text())
            value = min(500, max(1, value))
            while (500%value)!=0:
                value += 1
            orParams[1] = value
            value = int(self.lineSampleCount.text())
            orParams[2] = min(1000000, max(10000, value))
            #
            self.lineSampleRate.setText(str(orParams[0]))
            self.lineSampleOversample.setText(str(orParams[1]))
            self.lineSampleCount.setText(str(orParams[2]))
        except:
            orParams = None
        return orParams
    def SamplingOneSample(self):
        if self.stateAutoRunning or self.stateSamplingRunning:
            self.textStatus.append('A test is already running, ignoring request to run...')
            return False
        try:
            self.UpdateProgressSampling(0)
            if not self.nidaqHandler.parsedXML:
                self.SamplingConfigFileLoad()
            if not self.nidaqHandler.parsedXML:
                self.textStatus.append('Failed to run One Sample test, ' + \
                    'please enter a valid XML/PJDAQ file!!')
                return False
            orParams = self.BuildOverrideParams()
            packPlotVars = \
                [self.labelPlot1.text(), self.labelPlot2.text(), self.labelPlot3.text(), \
                self.labelPlot4.text(), self.labelPlot5.text(), self.labelPlot6.text(), \
                self.labelPlot7.text(), self.labelPlot8.text(), self.labelPlot9.text()]
            if self.chkSamplingOutputFile.isChecked():
                outputfilename = self.lineSamplingOutputFile.text()
                try:
                    os.remove(outputfilename)
                except:
                    pass
                if os.path.exists(outputfilename):
                    self.textStatus.append('Failed to run One Sample test, ' + \
                        'please manually remove output file (' + outputfilename + ')!!')
                    return False
            else:
                outputfilename = None
            if self.nidaqHandler.SampleOneSample( \
                outputfilename=outputfilename, packPlotVars=packPlotVars, \
                overrideParams=orParams):
                self.UpdateProgressSampling(100)
                packVipAndPlot = self.nidaqHandler.BuildVipAndPlotPack()
                self.UpdateVipAndPlot(packVipAndPlot)
                self.textStatus.append('Started and finished running One Sample test...')
                return True
            else:
                self.textStatus.append('Failed to run One Sample test!!')
                return False
        except:
            self.textStatus.append('Failed to run One Sample test!!')
            return False
    def SamplingGoHelper(self, live, usePool):
        if self.stateAutoRunning or self.stateSamplingRunning:
            self.textStatus.append('A test is already running, ignoring request to run...')
            return False
        if not self.nidaqHandler.parsedXML:
            self.SamplingConfigFileLoad()
        if not self.nidaqHandler.parsedXML:
            self.textStatus.append('Failed to run Sampling test, ' + \
                'please enter a valid XML/PJDAQ file!!')
            return False
        packPlotVars = [self.labelPlot1, self.labelPlot2, self.labelPlot3, \
            self.labelPlot4, self.labelPlot5, self.labelPlot6, \
            self.labelPlot7, self.labelPlot8, self.labelPlot9]  # note, the labels
        self.nidaqHandler.PopulateSamplingTable( \
            tableSampling=self.tableSampling, packPlotVars=packPlotVars)
        orParams = self.BuildOverrideParams()
        packPlotVars = \
            [self.labelPlot1.text(), self.labelPlot2.text(), self.labelPlot3.text(), \
            self.labelPlot4.text(), self.labelPlot5.text(), self.labelPlot6.text(), \
            self.labelPlot7.text(), self.labelPlot8.text(), self.labelPlot9.text()]  # note, variable names
        if self.chkSamplingOutputFile.isChecked():
            outputfilename = self.lineSamplingOutputFile.text()
            try:
                os.remove(outputfilename)
            except:
                pass
            if os.path.exists(outputfilename):
                self.textStatus.append('Failed to run Sampling test, ' + \
                    'please manually remove output file (' + outputfilename + ')!!')
                return False
        else:
            outputfilename = None
        if not self.nidaqHandler.StartSampling(outputfilename=outputfilename, \
            usePool=usePool, packPlotVars=packPlotVars, overrideParams=orParams, live=live):
            self.stateSamplingRunning = False
            self.textStatus.append('Failed to run Sampling test!!')
            return False
        else:
            self.stateSamplingRunning = True
            self.textStatus.append('Started Sampling test...')
            self.EnableSamplingUI(allowSampling=False)
            self.EnableAutomationUI(allowRunning=False, enableStopButton=False)
            if live:
                self.progSamplingOutput.setValue(50)  # always at 50
            return True
    def SamplingLive(self):
        return self.SamplingGoHelper(live=True, usePool=False)
    def SamplingGo(self):
        usePool = self.chkSamplingPool.isChecked()
        return self.SamplingGoHelper(live=False, usePool=usePool)
    def SamplingStop(self):
        if self.stateSamplingRunning:
            # note, self.stateSamplingRunning is set to False in TimerCallback()
            self.nidaqHandler.StopSampling()
        self.EnableSamplingUI(allowSampling=True)
        self.EnableAutomationUI(allowRunning=True)
        return True
    def TabMainChange(self):
        # if Large Plots, when user change tab from "NI DAQ", then change to Small plots
        if self.tabMain.currentIndex()!=2:  # non-"NI DAQ"
            if self.comboSamplingPlotOptions.currentText()!='No Plots':
                self.comboSamplingPlotOptions.setCurrentIndex(0)  # 'No Plots'
                # note, self.SamplingPlotOptionsChanged() will be triggered
    def PopulateSamplingFrame(self):
        self.comboSamplingFrame.clear()
        self.comboSamplingFrame.addItems(['No MovAvg', '1 msec MovAvg', \
            '5 msec MovAvg', '10 msec MovAvg', '12 msec MovAvg'])
        self.comboSamplingFrame.setCurrentIndex(0)
    def SamplingFrameChanged(self, value):
        movAvgFrame = None
        if value!='No MovAvg':
            value = value.replace(' msec MovAvg', '')
            try:
                movAvgFrame = int(value)
            except:
                movAvgFrame = None
        self.nidaqHandler.SetMovAvgFrame(movAvgFrameInMilliseconds=movAvgFrame)
    def PopulateSamplingPlotOptions(self):
        self.comboSamplingPlotOptions.clear()
        self.comboSamplingPlotOptions.addItems(['No Plots', \
            'Plot V', 'Plot I', 'Plot P', 'Plot V+I', 'Plot I+P', 'Plot V+I+P'])
        self.comboSamplingPlotOptions.setCurrentIndex(0)
        # dimensions of all options
        # [No Plots, Yes Plots], each with (note, only certains fg-components matter):
        #   [fgPlot, fgTableSampling, fgTabMain, fgGroupSampling]
        self.dimPlots = [None, None]
        fgPlotN = self.tableSampling.frameGeometry()
        fgTableSamplingN = self.tableSampling.frameGeometry()
        fgTabMainN = self.tabMain.frameGeometry()
        fgGroupSamplingN = self.groupSampling.frameGeometry()
        fgPlotN.setX(fgPlotN.x()+fgTabMainN.width())  # way off screen
        self.dimPlots[0] = [fgPlotN, fgTableSamplingN, fgTabMainN, fgGroupSamplingN]
        # Large: both tabMain and groupSampling to extend to where tabStatus ends
        fgPlotY = self.tableSampling.frameGeometry()
        fgTableSamplingY = self.tableSampling.frameGeometry()
        fgTabStatusY = self.tabStatus.frameGeometry()
        fgTabMainY = self.tabMain.frameGeometry()
        deltaDownward = (fgTabStatusY.y()+fgTabStatusY.height())-\
            (fgTabMainY.y()+fgTabMainY.height())
        fgTabMainY.setHeight(fgTabMainY.height()+deltaDownward)
        fgGroupSamplingY = self.groupSampling.frameGeometry()
        fgGroupSamplingY.setHeight(fgGroupSamplingY.height()+deltaDownward)
        # just below tableSampling, but slightly smaller so won't cover edge
        fgPlotY.setX(10)
        fgPlotY.setY(270)
        fgPlotY.setWidth(721)
        fgPlotY.setHeight(201)
        self.dimPlots[1] = [fgPlotY, fgTableSamplingY, fgTabMainY, fgGroupSamplingY]
    def SamplingPlotOptionsChanged(self, value):
        # note, expects self.dimPlots to contain...
        try:
            if value=='No Plots':
                newDim = self.dimPlots[0]
            else:
                newDim = self.dimPlots[1]
                value = value.replace('Plot ', '')
                value = value.replace('+', '')
                if value=='':
                    value = 'VIP'  # should not get here
                try:
                    self.plotSampling.SetMode(mode=value)
                except:
                    pass
            # note, fgPlot sets x/y/width/height, rest only sets width/height
            fgPlot = newDim[0]
            self.plotSampling.SetFrameGeometry(fgPlot)
            fgTableSampling = newDim[1]
            self.tableSampling.resize(fgTableSampling.width(), fgTableSampling.height())
            fgTabMain = newDim[2]
            self.tabMain.resize(fgTabMain.width(), fgTabMain.height())
            fgGroupSampling = newDim[3]
            self.groupSampling.resize(fgGroupSampling.width(), fgGroupSampling.height())
        except:
            return False
        return True
    def SamplingOverrideChanged(self, state):
        enable = (state==QtCore.Qt.Checked)
        self.lineSampleRate.setEnabled(enable)
        self.lineSampleOversample.setEnabled(enable)
        self.lineSampleCount.setEnabled(enable)
    def SamplingPushUpVars(self):
        packPlotVars = []
        listHeaders = self.nidaqHandler.listHeaders
        listChkPlot = self.nidaqHandler.listChkPlot
        for i in range(len(listChkPlot)):
            if listChkPlot[i].checkState() == QtCore.Qt.Checked:
                packPlotVars.append(listHeaders[i])
        while len(packPlotVars)<9:
            packPlotVars.append('')
        lookupLabelPlot = [self.labelPlot1, self.labelPlot2, self.labelPlot3, \
            self.labelPlot4, self.labelPlot5, self.labelPlot6, \
            self.labelPlot7, self.labelPlot8, self.labelPlot9]
        for i in range(9):
            lookupLabelPlot[i].setText(packPlotVars[i])
        return packPlotVars
    def SamplingReset(self):
        try:
            packPlotVars = self.SamplingPushUpVars()
            self.plotSampling.ClearPlotData()
            self.nidaqHandler.ResetVipAndPlot(packPlotVars=packPlotVars)
            packVipAndPlot = self.nidaqHandler.BuildVipAndPlotPack()
            self.UpdateVipAndPlot(packVipAndPlot)
        except:
            pass
    def SamplingFreeze(self):
        if self.visualFreeze==True:
            self.visualFreeze = False
            self.btnSamplingFreeze.setText('Freeze')
        else:
            self.visualFreeze = True
            self.btnSamplingFreeze.setText('Unfreeze')
    def SamplingClipboard(self):
        try:
            with self.nidaqHandler.lockVip:
                values = self.nidaqHandler.listHeaders
                line = ',' + ','.join(e for e in values) + os.linesep
                #
                values = self.nidaqHandler.vipData[1]
                line += 'V,' + \
                    ','.join("{0:.6g}".format(e) for e in values) + os.linesep
                values = self.nidaqHandler.vipData[2]
                line += 'I,' + \
                    ','.join("{0:.6g}".format(e) for e in values) + os.linesep
                values = self.nidaqHandler.vipData[3]
                line += 'P,' + \
                    ','.join("{0:.6g}".format(e) for e in values) + os.linesep
                # TOTAL_APU_POWER is self.nidaqHandler.vipData[4][0]
                values = self.nidaqHandler.vipData[4]
                line += os.linesep + os.linesep + 'TOTAL_APU_POWER,' + \
                    "{0:.6g}".format(values[0]) + os.linesep
                clipboard.copy(line)
        except:
            pass

    # Manual: TEC
    def TecComPortUpdate(self):
        tecPort = self.lineTecComPort.text()
        if tecPort=='':
            tecPort = None
        self.tec = SerialTec()
        self.tec.Setup(useThisPort=tecPort)
        if not self.tec.IsValid():
            self.textStatus.append('Error: Did not initialize TEC properly (' + tecPort + ')!!')
        else:
            if tecPort==None:
                tecPort = self.tec.ser.port
                self.lineTecComPort.setText(tecPort)
            self.textStatus.append('Initialized TEC properly (' + tecPort + ').')

    # Manual: AMD HDT Debugger
    def DebuggerIpUpdate(self):
        debuggerIp = self.lineDebuggerIp.text()
        pass  # todo

    # Manual: Display Resolution
    displayResolutions = OrderedDict([
        ('1080P', '1080P'),
        ('4K', '4K')])
    def PopulateResolutions(self, defaultResolution='1080P'):
        try:
            self.comboResolutions.clear()
            self.comboResolutions.addItems(list(self.displayResolutions.keys()))
        except:
            pass
    def ResolutionUpdate(self):
        app = self.comboDeployApps.currentText()
        try:
            if app=='1080P':
                pass
            elif app=='4K':
                pass
        except:
            pass
        pass  # todo

    # Manual: Xbox Console
    def EnableDiscoveryUI(self, discoveryGood, allowDiscovery, \
        enableDiscoverButton=None):
        if enableDiscoverButton!=None:
            self.btnConsoleDiscover.setEnabled(enableDiscoverButton)
        else:
            self.btnConsoleDiscover.setEnabled(allowDiscovery)
        self.btnConsolePingHost.setEnabled(discoveryGood)
        self.btnConsolePingSystem.setEnabled(discoveryGood)
        self.btnConsoleCommandSend.setEnabled(discoveryGood)
        self.btnAppDeploy.setEnabled(discoveryGood)
        self.btnAppDeployAll.setEnabled(discoveryGood)
        self.btnAppLaunch.setEnabled(discoveryGood)
        self.btnAppTerminate.setEnabled(discoveryGood)
        self.btnRailsSet.setEnabled(discoveryGood)
        self.btnRailsGet.setEnabled(discoveryGood)
    def ConsoleDiscover(self):
        if self.stateAutoRunning or self.stateSamplingRunning:
            self.textStatus.append('A test is already running, ignoring request to run...')
            return
        self.textKdhost.setText('')
        self.textKdsra.setText('')
        self.textKdera.setText('')
        self.textDsmc.setText('')
        self.lineConsoleHostIP.setText('(Discovery in progress)')
        self.lineConsoleSystemIP.setText('(Discovery in progress)')
        self.EnableDiscoveryUI(discoveryGood=False, \
            allowDiscovery=False, enableDiscoverButton=False)
        softFusing = self.chkConsoleSoftFusing.isChecked()
        hdtip = self.lineConsoleHdtip.text()
        tether = self.chkConsoleTether.isChecked()
        self.xboxStateMachine.DoDiscoverySequence( \
            guicomm=self.guicomm, hdtip=hdtip, softFusing=softFusing, \
            tether=tether)
        self.textStatus.append('Started Xbox Discovery...')
        self.stateAutoRunning = True
    def ConsolePingHost(self):
        if self.stateAutoRunning or self.stateSamplingRunning:
            self.textStatus.append('A test is already running, ignoring request to ping...')
            return
        try:
            if os.system('ping -n 1 '+self.lineConsoleHostIP.text())==0:
                self.btnConsolePingHost.setStyleSheet("background-color: green")
            else:
                self.btnConsolePingHost.setStyleSheet("background-color: red")
        except:
            self.btnConsolePingHost.setStyleSheet("background-color: yellow")
            pass
    def ConsolePingSystem(self):
        if self.stateAutoRunning or self.stateSamplingRunning:
            self.textStatus.append('A test is already running, ignoring request to ping...')
            return
        try:
            if os.system('ping -n 1 '+self.lineConsoleSystemIP.text())==0:
                self.btnConsolePingSystem.setStyleSheet("background-color: green")
            else:
                self.btnConsolePingSystem.setStyleSheet("background-color: red")
        except:
            self.btnConsolePingSystem.setStyleSheet("background-color: yellow")
            pass

    selectAnActionString = 'Select an action...'
    consoleActions = OrderedDict([
        (selectAnActionString, selectAnActionString),
        ('ResetCycle', '(ResetCycle)')])
    def PopulateConsoleActions(self, defaultAction='Select an action...'):
        try:
            self.comboConsoleAction.clear()
            self.comboConsoleAction.addItems(list(self.consoleActions.keys()))

            desc = self.consoleActions[defaultAction]
            self.labelConsoleActionDesc.setText(desc)
        except:
            self.labelConsoleActionDesc.setText('')
    def ConsoleActionChanged(self, value):
        try:
            desc = self.consoleActions[value]
            self.labelConsoleActionDesc.setText(desc)
        except:
            self.labelConsoleActionDesc.setText('')
    def ConsoleCommandSend(self):
        action = self.comboConsoleAction.currentText()
        try:
            if action=='ResetCycle':
                xbconnect.ResetCycle()
            else:
                pass
        except:
            pass

    selectAnAppString = 'Select an app...'
    lockDeployables = Lock()
    deployables = OrderedDict()  # key is name, value is (launch, terminate)
    def PopulateDeployApps(self):
        try:
            self.comboDeployApps.clear()
            self.deployables = OrderedDict([
                (self.selectAnAppString, None)])
            # directories under '.\Apps' (eg, '.\Apps\DeferredParticles')
            for dirname in glob.iglob('.\\Apps\\**', recursive=True):
                if not os.path.isfile(dirname):
                    if (dirname.count('\\')==2) and (dirname!='.\\Apps\\'):
                        dirname = dirname.replace('.\\Apps\\', '')
                        self.deployables[dirname] = None
            self.comboDeployApps.addItems(list(self.deployables.keys()))
            self.comboDeployApps.setCurrentIndex(0)
            #
            self.PopulateLaunchTerminateApps()
            return True
        except:
            self.comboDeployApps.clear()
            self.comboLaunchTerminateApps.clear()
        return False
    def PopulateLaunchTerminateApps(self):
        try:
            self.comboLaunchTerminateApps.clear()
            appsForLaunchAndTerminate = None
            for name, value in self.deployables.items():
                if value!=None:
                    if appsForLaunchAndTerminate==None:
                        appsForLaunchAndTerminate = [self.selectAnAppString]
                    appsForLaunchAndTerminate.append(name)
            if appsForLaunchAndTerminate!=None:
                self.comboLaunchTerminateApps.addItems(appsForLaunchAndTerminate)
            return True
        except:
            self.comboLaunchTerminateApps.clear()
        return False
    def AppDeploy(self):
        if (self.xboxStateMachine==None):
            return False
        app = self.comboDeployApps.currentText()
        try:
            if (app!=self.selectAnAppString):
                self.xboxStateMachine.xbconsole.XbAppDeploy(app)
                self.deployables[app] = \
                    (self.xboxStateMachine.xbconsole.ConsoleDepPackageName, \
                    self.xboxStateMachine.xbconsole.ConsoleDepPackageID)
                self.PopulateLaunchTerminateApps()
                self.textStatus.append('Deployed Xbox app (' + app + ').')
                return True
        except:
            self.textStatus.append('Error in deploying Xbox app!!')
        return False
    def AppDeployAllThreadable(self):
        with self.lockDeployables:
            deployablesNew = self.deployables.copy()
        try:
            for app in deployablesNew.keys():
                if app!=self.selectAnAppString:
                    self.xboxStateMachine.xbconsole.XbAppDeploy(app)
                    deployablesNew[app] = (self.xboxStateMachine.xbconsole.ConsoleDepPackageName, \
                        self.xboxStateMachine.xbconsole.ConsoleDepPackageID)
            with self.lockDeployables:
                self.deployables = deployablesNew
            self.PopulateLaunchTerminateApps()
            self.textStatus.append('Deployed all Xbox apps.')
            return True
        except:
            self.textStatus.append('Error in deploying all Xbox apps!!')
        return False
    def AppDeployAll(self):
        if (self.xboxStateMachine==None):
            return False
        self.textStatus.append('Started deploying all Xbox apps...')
        threading.Thread(target=self.AppDeployAllThreadable).start()
        return True
    def AppLaunch(self):
        if (self.xboxStateMachine==None):
            return False
        app = self.comboLaunchTerminateApps.currentText()
        try:
            if self.deployables[app]!=None:
                launch, terminate = self.deployables[app]
                self.xboxStateMachine.xbconsole.ConsoleDepPackageName = launch
                self.xboxStateMachine.xbconsole.ConsoleDepPackageID = terminate
                threading.Thread(target=self.xboxStateMachine.xbconsole.XbApplaunch).start()
                self.textStatus.append('Launched Xbox app.')
                return True
        except:
            pass
        return False
    def AppTerminate(self):
        if (self.xboxStateMachine==None):
            return False
        app = self.comboLaunchTerminateApps.currentText()
        try:
            if self.deployables[app]!=None:
                launch, terminate = self.deployables[app]
                self.xboxStateMachine.xbconsole.ConsoleDepPackageName = launch
                self.xboxStateMachine.xbconsole.ConsoleDepPackageID = terminate
                self.xboxStateMachine.xbconsole.XbAppTerminate()
                self.textStatus.append('Terminated Xbox app.')
                return True
        except:
            pass
        return False

    # TEC
    # note, infoTemp is 
    #   [tecTarget, dieTarget, tecActual, dieActual, tecReadFails, dieReadFails]
    def SetPackageTemp(self):
        value = round(self.spinPackageTemp.value(),1)
        self.tec.SetTemp(value)
        self.infoTemp[0] = value
    def SetDieTemp(self):
        value = round(self.spinDieTemp.value(),1)
        self.infoTemp[1] = value
    def DieTempAutoAdjustChanged(self, state):
        checked = (state==QtCore.Qt.Checked)
        self.spinDieTemp.setEnabled(checked)
        self.btnSetDieTemp.setEnabled(checked)
        self.chkDieTempStopWhenStable.setEnabled(checked)
        self.infoTempAutoAdjust[0] = checked
        self.infoTempAutoAdjust[2] = 0
    def DieTempStopWhenStableChanged(self, state):
        checked = (state==QtCore.Qt.Checked)
        self.infoTempAutoAdjust[1] = checked
        self.infoTempAutoAdjust[2] = 0
    # Screenshot
    def ScreenshotOnOffChanged(self):
        self.doScreenshotUpdate = not self.doScreenshotUpdate
        if not self.doScreenshotUpdate:
            try:
                self.btnScreenshot.setIcon(QtGui.QIcon('.\\XboxLogo.png'))
                self.btnScreenshot.setIconSize(QtCore.QSize(161, 71))
            except:
                pass

    # Rails
    selectABoardTypeString = 'Select a board type...'
    dictRailsBoardTypes = OrderedDict([ \
            (selectABoardTypeString, None), \
            ('CactusFabEPlus (Cactus fab E+/Coorg fab D+ Production)', 'CactusFabEPlus'), \
            ('CSCBFabDPlus (Cactus SCB fab D+)', 'CSCBFabDPlus') ])
    def PopulateRailsBoardTypes(self):
        self.comboRailsBoardType.clear()
        self.comboRailsBoardType.addItems(self.dictRailsBoardTypes.keys())
    def RailsSet(self):
        try:
            Vregobj = Vregscontrol.VRegs()
            Vregobj.ftdiserial = self.xboxStateMachine.xbconsole.Ftdi_Serial
            Vregobj.boardtype = self.dictRailsBoardTypes[self.comboRailsBoardType.currentText()]
            if Vregobj.boardtype==None:
                self.textStatus.append('Please pick a board type to set Rails voltages...')
                return False
        except:
            return False
        retValue = True
        if self.chkGfx.isChecked():
            try:
                value = self.spinGfx.value()
                Vregobj.setvoltage("GFX", "dsmcdbg", value)
                self.textStatus.append('Set Rails GFX voltage to ' + value + ' mV.')
            except:
                retValue = False
        if self.chkCpu.isChecked():
            try:
                value = self.spinCpu.value()
                Vregobj.setvoltage("CPU", "dsmcdbg", value)
                self.textStatus.append('Set Rails CPU voltage to ' + value + ' mV.')
            except:
                retValue = False
        if self.chkNbsoc.isChecked():
            try:
                value = self.spinNbsoc.value()
                Vregobj.setvoltage("SOC", "dsmcdbg", value)
                self.textStatus.append('Set Rails SOC voltage to ' + value + ' mV.')
            except:
                retValue = False
        if self.chkMemphy.isChecked():
            try:
                value = self.spinMemphy.value()
                Vregobj.setvoltage("MEMPHY", "xbvregs", value)
                self.textStatus.append('Set Rails MEMPHY voltage to ' + value + ' mV.')
            except:
                retValue = False
        return retValue
    def RailsGet(self):
        try:
            Vregobj = Vregscontrol.VRegs()
            Vregobj.ftdiserial = self.xboxStateMachine.xbconsole.Ftdi_Serial
            Vregobj.boardtype = self.dictRailsBoardTypes[self.comboRailsBoardType.currentText()]
            if Vregobj.boardtype==None:
                self.textStatus.append('Please pick a board type to get Rails voltages...')
                return False
        except:
            return False
        retValue = True
        if self.chkGfx.isChecked():
            try:
                value = str(int(float(Vregobj.readvoltage("GFX"))*1000))
                self.lineGfxVolt.setText(value)
                self.textStatus.append('Got Rails GFX voltage, ' + value + ' mV.')
            except:
                retValue = False
        if self.chkCpu.isChecked():
            try:
                value = str(int(float(Vregobj.readvoltage("CPU"))*1000))
                self.lineCpuVolt.setText(value)
                self.textStatus.append('Got Rails CPU voltage, ' + value + ' mV.')
            except:
                retValue = False
        if self.chkNbsoc.isChecked():
            try:
                value = str(int(float(Vregobj.readvoltage("SOC"))*1000))
                self.lineNbVolt.setText(value)
                self.textStatus.append('Got Rails SOC voltage, ' + value + ' mV.')
            except:
                retValue = False
        if self.chkMemphy.isChecked():
            try:
                value = str(int(float(Vregobj.readvoltage("MEMPHY"))*1000))
                self.lineMemphyVolt.setText(value)
                self.textStatus.append('Got Rails MEMPHY voltage, ' + value + ' mV.')
            except:
                retValue = False
        return retValue

    # Automation
    def EnableAutomationUI(self, allowRunning, enableStopButton=None):
        self.btnAutoGo.setEnabled(allowRunning)
        if enableStopButton==None:
            self.btnAutoStop.setEnabled(not allowRunning)
        else:
            self.btnAutoStop.setEnabled(enableStopButton)
        self.btnAutoConfigFileBrowse.setEnabled(allowRunning)
        self.btnAutoConfigFileLoad.setEnabled(allowRunning)
        self.btnAutoFileBrowse.setEnabled(allowRunning)
        self.btnAutoFileLoad.setEnabled(allowRunning)
    def PopulateAutoRailsBoardTypes(self):
        self.comboAutoRailsBoardType.clear()
        self.comboAutoRailsBoardType.addItems(self.dictRailsBoardTypes.keys())
    def AutoConfigFileBrowse(self):
        filename = self.lineAutoConfigFile.text()
        try:
            filespec = QFileDialog.getOpenFileName(self, \
                filename, './', 'PJDaq Files(*.PJDaq)')
            if filespec[0]=='':
                filespec[0] = filename
            self.lineAutoConfigFile.setText(filespec[0])
        except:
            pass
    def AutoConfigFileLoad(self):
        configFilename = self.lineAutoConfigFile.text()
        if not self.nidaqHandler.ParseNidaqXml(filename=configFilename):
            self.textStatus.append('Failed to load configuration/XML file (' + configFilename + ')!!')
        else:
            self.textStatus.append('Successfully loaded configuration/XML file (' + configFilename + ').')
    def AutoFileBrowse(self):
        filename = self.lineAutoFile.text()
        try:
            filespec = QFileDialog.getOpenFileName(self, \
                filename, './', 'CSV Files(*.csv)')
            if filespec[0]=='':
                filespec[0] = filename
            self.lineAutoFile.setText(filespec[0])
        except:
            pass
    def AutoFileLoad(self):
        testFilename = self.lineAutoFile.text()
        if self.xboxStateMachine.ParseTestsCsv(testFilename, self.tableAutoFile):
            self.textStatus.append('Successfully loaded test file (' + testFilename + ').')
        else:
            self.textStatus.append('Error in loading test file (' + testFilename + ').')
            errors = self.xboxStateMachine.GetErrors()
            for error in errors:
                self.textStatus.append(error)
    def AutoGo(self):
        if self.comboAutoRailsBoardType.currentText()==self.selectABoardTypeString:
            self.textStatus.append('Failed to run Automation test, please select a board type!!')
            return
        if self.stateAutoRunning or self.stateSamplingRunning:
            self.textStatus.append('A test is already running, ignoring request to run...')
            return
        self.textKdhost.setText('')
        self.textKdsra.setText('')
        self.textKdera.setText('')
        self.textDsmc.setText('')
        testFilename = self.lineAutoFile.text()
        autoOneSample = self.chkAutoOneSample.isChecked()
        packInfoTemp = [self.infoTemp, self.infoTempAutoAdjust, \
            self.timeBetweenTempAdjustsInSeconds, self.tempStableRange, \
            self.tempAdjustRange, self.tempStableCountNeeded]
        autoSkipTemp = self.chkAutoSkipTemp.isChecked()
        configFilename = self.lineAutoConfigFile.text()
        boardType = self.dictRailsBoardTypes[self.comboAutoRailsBoardType.currentText()]
        knownErrorFilenames = self.lineAutoKnownErrorFiles.text()
        hdtip = self.lineAutoHdtip.text()
        softFusing = self.chkAutoSoftFusing.isChecked()
        tether = self.chkAutoTether.isChecked()
        usePool = self.chkAutoPool.isChecked()
        self.stateAutoRunning = self.xboxStateMachine.DoAutoSequence( \
            guicomm=self.guicomm, nidaqHandler=self.nidaqHandler, \
            configFilename=configFilename, boardType=boardType, \
            testFilename=testFilename, tableAutoFile=self.tableAutoFile, \
            knownErrorFilenames=knownErrorFilenames, tec=self.tec, \
            autoOneSample=autoOneSample, packInfoTemp=packInfoTemp, \
            autoSkipTemp=autoSkipTemp, hdtip=hdtip, softFusing=softFusing, \
            tether=tether, usePool=usePool)
        if self.stateAutoRunning:
            self.textStatus.append('Started Automation test sequence...')
            self.EnableDiscoveryUI(discoveryGood=False, \
                allowDiscovery=False, enableDiscoverButton=False)
            self.EnableAutomationUI(allowRunning=False, enableStopButton=True)
            self.EnableSamplingUI(allowSampling=False, enableStopButton=False)
        else:
            self.textStatus.append('Failed to run Automation test sequence!!')
            errors = self.xboxStateMachine.GetErrors()
            for error in errors:
                self.textStatus.append(error)
    def AutoStop(self):
        if self.stateAutoRunning:
            self.stateAutoRunning = False
            self.textStatus.append('Stopped Automation test sequence.')
            self.EnableDiscoveryUI(discoveryGood=False, allowDiscovery=True)
            self.EnableAutomationUI(allowRunning=True)
            self.EnableSamplingUI(allowSampling=True)

class SerialTec():
    WRITE_OP = 6
    READ_OP = 3
    defaultComPort = 'COM3'

    lockPort = Lock()
    ser = None

    def AutoDetectTecPort(self):
        try:
            ports = sorted(list(serial.tools.list_ports.comports()))
            for device, desc, hwid in ports: 
                if 'Prolific' in desc:
                    return device
        except:
            pass
        return self.defaultComPort
    def Setup(self, useThisPort=None):
        with self.lockPort:
            try:
                self.ser = serial.Serial()
                if useThisPort==None:
                    self.ser.port = self.AutoDetectTecPort()
                else:
                    self.ser.port = useThisPort
                self.ser.baudrate = 19200
                self.ser.bytesize = serial.EIGHTBITS  # number of bits per bytes
                self.ser.parity = serial.PARITY_NONE  # set parity check: no parity
                self.ser.stopbits = serial.STOPBITS_ONE  # number of stop bits
                #self.ser.timeout = None  # block read
                self.ser.timeout = 1  # non-block read
                #self.ser.timeout = 2  # timeout block read
                self.ser.xonxoff = False  # disable software flow control
                self.ser.rtscts = False  # disable hardware (RTS/CTS) flow control
                self.ser.dsrdtr = False  # disable hardware (DSR/DTR) flow control
                self.ser.writeTimeout = 2  # timeout for write

                self.ser.open()
                try:
                    # flush input buffer, discarding all its contents
                    self.ser.flushInput()
                    # flush output buffer, aborting current output 
                    # and discard all that is in buffer
                    self.ser.flushOutput()
                    return True
                except:
                    pass
            except:
                self.ser = None
        return False
    def IsValid(self):
        with self.lockPort:
            return (self.ser != None) and (self.ser.isOpen())
    def ModRTU_CRC(self, buf, length):
        crc = 0xFFFF
        for pos in range(0, length):
            crc ^= buf[pos] # XOR byte into least sig. byte of crc
            for i in range(8, 0, -1):
                # Loop over each bit
                if ((crc & 0x0001) != 0):
                    # If the LSB is set
                    crc >>= 1 # Shift right and XOR 0xA001
                    crc ^= 0xA001
                else: # Else LSB is not set
                    crc >>= 1 # Just shift right
        # Note, this number has low and high bytes swapped, so use it accordingly (or swap bytes)
        return crc
    def BuildPacket(self, ID, WriteOp, ParmAddr, DataOrCount):
        Buffer = 8 * ['X'] # byte[8]
        CRC = 0
        #
        Buffer[0] = ID;
        if (WriteOp):
            Buffer[1] = self.WRITE_OP
        else:
            Buffer[1] = self.READ_OP
        Buffer[2] = ((ParmAddr >> 8) & 0xff)
        Buffer[3] = (ParmAddr & 0xff)
        Buffer[4] = ((DataOrCount >> 8) & 0xff)
        Buffer[5] = (DataOrCount & 0xff)
        CRC = self.ModRTU_CRC(Buffer, 6)
        Buffer[6] = (CRC & 0xff)
        Buffer[7] = ((CRC >> 8) & 0xff)
        #
        buf = bytearray()
        for i in range(8):
            buf.append(Buffer[i])
        return buf
    def SetTemp(self, temp):
        if self.IsValid():
            try:
                # write data
                cmdToSend = self.BuildPacket(ID=1, WriteOp=True, ParmAddr=0, DataOrCount=int(temp*10))
                with self.lockPort:
                    self.ser.write(cmdToSend)
                return True
            except:
                pass
        return False
    def GetTemp(self, timeout=0.5):
        if self.IsValid():
            try:
                timeStart = time.time()
                response = []
                # send a read, then wait for response
                cmdToSend = self.BuildPacket(ID=1, WriteOp=False, ParmAddr=0x1000, DataOrCount=1)
                self.ser.write(cmdToSend)
                while time.time() - timeStart <= timeout:
                    try:
                        with self.lockPort:
                            line = self.ser.readline()
                    except:
                        pass
                    if len(line) > 0:
                        response = list(line)
                #
                temp = None
                length = len(response)
                if len(response) >= 8:
                    temp = response[4] << 8
                    temp = temp | (response[5]&0xff)
                    temp /= 10.0
                    # check CRC
                    crcCalc = self.ModRTU_CRC(response, 6)
                    crcPacket = ((response[7]&0xFF)<<8)|(response[6]&0xFF)
                    if crcCalc != crcPacket:
                        return None
                    return temp
            except:
                pass
        return None
    # AskTemp()+ReceiveTemp() is equivalent of GetTemp() but without polling delays
    def AskTemp(self):
        if self.IsValid():
            try:
                response = []
                # send a read, then wait for response
                cmdToSend = self.BuildPacket(ID=1, WriteOp=False, ParmAddr=0x1000, DataOrCount=1)
                self.ser.write(cmdToSend)
            except:
                return False
        return True
    def ReceiveTemp(self):
        if self.IsValid():
            try:
                with self.lockPort:
                    line = self.ser.readline()
                    if len(line) > 0:
                        response = list(line)
                #
                temp = None
                length = len(response)
                if len(response) >= 8:
                    temp = response[4] << 8
                    temp = temp | (response[5]&0xff)
                    # check negative
                    if (temp&0x8000)!=0:
                        temp = temp - 65535
                    temp /= 10.0
                    # check CRC
                    crcCalc = self.ModRTU_CRC(response, 6)
                    crcPacket = ((response[7]&0xFF)<<8)|(response[6]&0xFF)
                    if crcCalc != crcPacket:
                        return None
                    return temp
            except:
                pass
        return None


class NidaqHandler():
    # fields of interest from XML file
    infoRawInputChannel = {'taskIndex', 'actualName', 'name', 'nickname', 'TerminalConfig', 'minVoltage', 'maxVoltage', 'varIndex', 'enabled', 'virtualIndex'}
    infoAnalogOutputChannel = {'taskIndex', 'actualName', 'enabled'}
    infoOutputChannel = {'name', 'enabled', 'DependsOn', 'numRequiredInputDevices', 'FormulaString', 'VariableIndex', 'TaskIndex'}
    # parsed info
    parsedXML = False
    dictSetupStruct = dict()
    dictRawInputChannel = OrderedDict()
    dictAnalogOutputChannel = OrderedDict()
    dictOutputChannel = OrderedDict()
    dictOutputChannelFormula = OrderedDict()
    # "pre-compiled" way to execute calculation given dependency checking
    listDependsOnOrderByName = []
    dictDerivedFormula = OrderedDict()
    # sampling variables (to be overwritten by values in XML file)
    sampleRate = 36000
    sampleOversample = 1
    sampleCountMax = 27778
    samplesPerChan = 500
    hardMaxSamplesFlushed = 1000000  # max samples to be flushed
    neededSamplesForMovAvg = 1
    # callback variables
    numSamplesAcquired = 0
    numSamplesFlushed = 0
    # sampling variables
    lockSamplesHeld = Lock()
    samplesHeld = []
    inTask = None
    # visualization
    visualFreeze = False
    lockVip = Lock()
    vipData = [None] * 5  # [header, V, I, P, totalPower], each a list of values, except header
    lookupVipIndex = [None] * 5  # [header, V, I, P, totalPower], each a list of index, except header
    plotData = [[None]*9 for i in range(3)]  # 3 plots, each have 4 values to plot (to match plotBuffer, kind of)
    lookupPlotIndex = [[None]*9 for i in range(3)]  # 3 plots, each have 9 values to plot (to match plotBuffer, kind of)
    refreshPeriod = 12  # 1X/sec
    # whether killed by user
    killStatus = False

    def LookupTermConfig(self, type):
        type = type.upper()
        if type == 'DIFFERENTIAL':
            termconfig = nidaqmx.constants.TerminalConﬁguration.DIFFERENTIAL
        elif type == 'RSE':
            termconfig = nidaqmx.constants.TerminalConﬁguration.RSE
        elif type == 'NRSE':
            termconfig = nidaqmx.constants.TerminalConﬁguration.NRSE
        elif type == 'PSEUDODIFFERENTIAL':
            termconfig = nidaqmx.constants.TerminalConﬁguration.PSEUDODIFFERENTIAL
        else:
            termconfig = nidaqmx.constants.TerminalConﬁguration.DEFAULT
        return termconfig
    def ParseNidaqXml(self, filename):
        self.parsedXML = True
        try:
            self.dictSetupStruct = dict()
            self.dictRawInputChannel = OrderedDict()
            self.dictAnalogOutputChannel = OrderedDict()
            self.dictOutputChannel = OrderedDict()
            self.dictOutputChannelFormula = OrderedDict()
            self.listDependsOnOrderByName = []
            tree = ET.parse(filename)
            root = tree.getroot()
            for item in root:
                self.dictSetupStruct[item.tag] = item.text
            self.projectName = self.dictSetupStruct['ProjectName']
            self.sampleRate = int(self.dictSetupStruct['SampleRateValue'])
            self.sampleCountMax = int(self.dictSetupStruct['MAX_SAMPLES_PER_CHANNEL'])
            self.sampleOversample = int(self.dictSetupStruct['overSampleRate'])
            self.samplesPerChan = 500
            for item in root.iter('RawInputChannel'):
                dictInfo = {}
                for info in self.infoRawInputChannel:
                    try:
                        value = item.find(info).text
                        if info=='varIndex':
                            valueIndex = value
                    except:
                        value = ''
                    dictInfo[info] = value
                if dictInfo.get('enabled', 'false') == 'true':
                    actualName = dictInfo['actualName']
                    self.dictRawInputChannel[actualName] = dictInfo
            for item in root.iter('AnalogOutputChannel'):
                dictInfo = {}
                for info in self.infoAnalogOutputChannel:
                    try:
                        value = item.find(info).text
                    except:
                        value = ''
                    dictInfo[info] = value
                actualName = dictInfo['actualName']
                self.dictAnalogOutputChannel[actualName] = dictInfo
            listDerived = []
            valueIndex = '0'
            for item in root.findall('./outputs/OutputChannel'):
                dependsOnList = []
                try:
                    for dependsOnItem in item.findall('./DependsOn/int'):
                        dependsOnList.append(int(dependsOnItem.text))
                except:
                    dependsOnList = []
                dictInfo = {}
                for info in self.infoOutputChannel:
                    try:
                        if info=='DependsOn':
                            value = dependsOnList
                        else:
                            value = item.find(info).text
                        if info=='VariableIndex':
                            valueIndex = value
                    except:
                        value = ''
                    dictInfo[info] = value
                if dictInfo.get('enabled', 'false') == 'true':
                    name = dictInfo['name']
                    self.dictOutputChannel[name] = dictInfo
                    self.dictOutputChannelFormula[name] = dictInfo.get('FormulaString', '0')
                    #
                    try:
                        valueIndex = int(valueIndex)
                        listDerived.append(valueIndex)
                    except:
                        valueIndex = 0
            # go build a DependsOn evaluation order list
            # algorithm: knock out those in the Derived list with only dependencies already knocked out,
            #   then just keep repeating above step until all Derived knocked out.
            #   the output listDependsOnOrderByName is the order to calculate the Derived list
            self.listDependsOnOrderByName = []
            avoidCircularCount = 10
            while len(listDerived)>0:
                if avoidCircularCount<=0:
                    self.parsedXML = False
                    break
                avoidCircularCount -= 1
                for name, info in self.dictOutputChannel.items():
                    valueIndex = int(info['VariableIndex'])
                    if valueIndex in listDerived:  # try to knock out, if haven't
                        # if it depends on anything that hasn't been knocked out,
                        #   then we cannot remove it, at least not at this point.
                        canRemove = True
                        for dependsOn in info['DependsOn']:
                            if dependsOn in listDerived:
                                canRemove = False
                                break
                        if canRemove:
                            listDerived.remove(valueIndex)
                            self.listDependsOnOrderByName.append(name)
            if not self.SetupDerived():
                self.parsedXML = False
        except:
            self.parsedXML = False
        return self.parsedXML
    def SetupVipIndex(self):
        self.lookupVipIndex = [None] * 5
        self.lookupVipIndex[0] = ['GFX','CPU','SOC','MEMP','MEMIO','1p8','SOCPHY','FUSE','3p3']  # header
        self.lookupVipIndex[1] = ['SOC_GFX_PROBE_V', 'SOC_CORE_PROBE_V', 'SOC_NBCORE_S_V', \
            'SOC_MEMPHY_PROBE_V', 'SOC_MEMIO_S_V', '1P8_VREG_V', 'SOC_PHY_S_V', \
            'FUSE_VREG_V', '3P3_VREG_V']  # V
        self.lookupVipIndex[2] = ['GFX_Total_I', 'CPUCORE_I', 'NBCORE_I', \
            'MEMPHY_I', 'MEMIO_I', '1P8_I', 'SOCPHY_I', 'FUSE_I', '3P3_I']  # I
        self.lookupVipIndex[3] = ['GFXCORE_P', 'CPUCORE_P', 'NBCORE_P', \
            'MEMPHY_P', 'MEMIO_P', '1P8_P', 'SOCPHY_P', 'FUSE_P', '3P3_P']  # P
        self.lookupVipIndex[4] = ['TOTAL_APU_POWER', 'TOTAL_IO_POWER'] + [None]*7  # totalPower, keep size consistent
        # get index of above names
        fullList = list(e['nickname'] for e in self.dictRawInputChannel.values()) + \
            list(self.dictOutputChannel.keys())
        notFoundItems = []
        for row in range(1, 5):
            for col in range(len(self.lookupVipIndex[row])):
                name = self.lookupVipIndex[row][col]
                if name==None:
                    continue
                found = False
                for index in range(len(fullList)):
                    if name==fullList[index]:
                        self.lookupVipIndex[row][col] = index
                        found = True
                        break
                if not found:  # should not get here
                    notFoundItems.append(name)
                    self.lookupVipIndex[row][col] = None
        #
        with self.lockVip:
            self.vipData = [None] * 5
            self.vipData[0] = list(self.lookupVipIndex[0])  # header
            for i in range(1, 5):
                self.vipData[i] = [None] * len(self.lookupVipIndex[i])
    def PopulateSamplingTable(self, tableSampling, packPlotVars):
        if not self.parsedXML:
           return False
        tableSampling.clear()
        self.SetupVipIndex()
        #
        tableSampling.setRowCount(4)
        tableSampling.setVerticalHeaderLabels(['V', 'I', 'P', 'Plot?'])
        #
        self.listHeaders = self.lookupVipIndex[0]
        colCount = len(self.listHeaders)
        tableSampling.setColumnCount(colCount)
        tableSampling.setHorizontalHeaderLabels(self.listHeaders)
        self.listChkPlot = []
        for i in range(colCount):
            tableSampling.setColumnWidth(i, 60)
            #
            chkPlot = QTableWidgetItem()
            chkPlot.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            if i<9:
                chkPlot.setCheckState(QtCore.Qt.Checked)       
                packPlotVars[i].setText(self.listHeaders[i])
            else:
                chkPlot.setCheckState(QtCore.Qt.Unchecked)       
            tableSampling.setItem(3, i, chkPlot)
            self.listChkPlot.append(chkPlot)
        return True
    def SetupTask(self):
        if not self.parsedXML:
            return None
        task = nidaqmx.Task()
        for chan, info in self.dictRawInputChannel.items():
            physical_channel = info['actualName']
            terminal_conﬁg = self.LookupTermConfig(info['TerminalConfig'])
            min_val = float(info['minVoltage'])
            max_val = float(info['maxVoltage'])
            task.ai_channels.add_ai_voltage_chan(physical_channel=physical_channel, \
                name_to_assign_to_channel='', terminal_conﬁg=terminal_conﬁg, \
                min_val=min_val, max_val=max_val, \
                units=nidaqmx.constants.VoltageUnits.VOLTS)
        return task
    def StartSampling(self, outputfilename, usePool, \
        packPlotVars=None, overrideParams=None, live=False):
        self.live = live
        self.usePool = usePool
        if overrideParams!=None:
            sampleRate, sampleOversample, sampleCountMax = overrideParams
            self.sampleRate = sampleRate
            self.sampleOversample = sampleOversample 
            self.sampleCountMax = sampleCountMax
        self.numSamplesAcquired = 0
        self.numSamplesFlushed = 0
        self.samplesHeld = []
        self.trueTimestamp0 = None
        self.poolBlockNumber = 0
        self.outputfilename = outputfilename
        self.killStatus = False
        self.ResetVipAndPlot(packPlotVars=packPlotVars)

        self.inTask = self.SetupTask()
        if self.inTask==None:
            return False
        try:
            if self.live:  # live, 1Hz (1 sample per second)
                self.sampleRate = 1
                self.samplesPerChan = 1
            self.inTask.timing.cfg_samp_clk_timing(
                rate=self.sampleRate,
                active_edge=nidaqmx.constants.Edge.RISING,
                sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
                samps_per_chan=self.samplesPerChan)
            if self.outputfilename!=None:
                # write to file, just header
                headers = self.GenerateHeaders()
                with open(self.outputfilename, 'w') as outputfile:
                    for header in headers:
                        print(header, file=outputfile)
                outputfile.close()
            self.inTask.register_every_n_samples_acquired_into_buffer_event(
                sample_interval=self.samplesPerChan, callback_method=self.Callback)
            self.inTask.start()
            self.doneSampling = False
        except:
            return False
        return True
    def GenerateHeaders(self):
        headers = ['#AGILENTDATALOGGER']
        #
        header = '#Timestamp,Seconds,' + ','.join(str(x['nickname']) for x in self.dictRawInputChannel.values())
        header = header + "," + ','.join(str(x['name']) for x in self.dictOutputChannel.values())
        headers.append(header)
        # eg, "101(Time stamp),101(Seconds),100(VDC),101(VDC),102(VDC),....."
        header = '101(Time stamp),101(Seconds)'
        for i in range(len(self.dictRawInputChannel)+len(self.dictOutputChannel)):
            header = header + "," + str(100+i) + '(VDC)'
        headers.append(header)
        return headers

    poolCleanupFlag = False
    poolThreadCount = 5  # 5-10 threads seem optimal for a 4-core
    poolSignalStart = Lock()
    poolSignalDone = Lock()
    poolLock = Lock()
    poolTimestamp0 = None
    poolRawBlock = None
    poolSampleBlock = None
    poolDerivedBlock = None
    poolLineBlock = None  # key off this, to know if started/done
    poolBlockNumber = 0
    poolDoneCount = 0
    def SetupPoolThreads(self):
        self.poolSignalStart.acquire()  # to match release in PoolCleanup
        self.PoolCleanup()
        #
        self.poolCleanupFlag = False
        self.poolSignalStart.acquire()  # puts threads to sleep initially
        for i in range(self.poolThreadCount):
            threading.Thread(target=self.PoolThreadFunc).start()
    def PoolCleanup(self):
        self.poolCleanupFlag = True
        try:
            self.poolSignalStart.release()
            time.sleep(0.25)
        except:
            pass
    def PoolThreadFunc(self):
        index = None
        while True:
            if index==None:
                with self.poolSignalStart:  # wait to be awakened
                    pass
                numVariables = len(self.dictRawInputChannel)
            if self.poolCleanupFlag:
                return 0  # only way out
            # figure out which sample to process, continue where last loop left off
            try:
                with self.poolLock:
                    if self.poolDoneCount<500:
                        if index==None:
                            i = 0
                        else:
                            i = index + 1
                        index = None
                        while i<500:
                            if self.poolLineBlock[i]==None:
                                self.poolLineBlock[i] = False  # mark starting
                                index = i
                                break
                            i += 1
                    else:
                        index = None
            except:
                index = None
            if index==None:  # back to sleep, wait for next block
                continue
            if self.poolCleanupFlag:
                return 0  # only way out
            # process poolRawBlock[x][y] to get poolSampleBlock[index]
            sample = [0.0] * numVariables
            try:
                rawBlock = self.poolRawBlock
                for v in range(numVariables):  # variables / column
                    sample[v] = rawBlock[v][index]
                self.poolSampleBlock[index] = sample  # no need to lock
            except:
                pass
            # if oversample, skip derived/lines generation
            if self.poolOversample!=1:
                line = ''
            else:
                # process poolSampleBlock[index] to get poolDerivedBlock[index]
                try:
                    derived = self.GenerateDerived(sample)
                    self.poolDerivedBlock[index] = derived  # no need to lock
                except:
                    derived = [0.0] * len(self.dictOutputChannel)
                # process sample+derived to get poolLineBlock[index]
                try:
                    with self.poolLock:
                        blockNumber = self.poolBlockNumber
                    sec = ((blockNumber * 500) + index) / self.sampleRate
                    line = self.trueTimestamp0.strftime("%#m/%#d/%Y %H:%M") + \
                        "," + "{0:.6g}".format(sec)
                    line = line + "," + ','.join("{0:.6g}".format(e) for e in sample)
                    line = line + "," + ','.join("{0:.6g}".format(e) for e in derived)
                except:
                    line = ''
            try:
                with self.poolLock:
                    self.poolLineBlock[index] = line  # mark done
                    self.poolDoneCount += 1
                    if self.poolDoneCount==500:  # finished very last one
                        self.poolSignalDone.release()
                    elif self.poolDoneCount==50:
                        # partially thru, prevent further unnecessary awakenings,
                        # so as to avoid unnecessary busy-looping.
                        # this may need more debugging and optimization
                        self.poolSignalStart.acquire()
            except:
                pass
    def PoolGeneratedDerivedBlock(self, rawBlock, poolOversample=1):
        with self.poolLock:
            self.poolDoneCount = 0
            self.poolOversample = poolOversample
            self.poolRawBlock = rawBlock
            self.poolSampleBlock = [None] * 500
            self.poolDerivedBlock = [None] * 500
            self.poolLineBlock = [None] * 500
        self.poolSignalDone.acquire()  # sleep (on acquire below) until threads done
        self.poolSignalStart.release()  # wake up threads
        with self.poolSignalDone:  # wait for threads done
            pass
        with self.poolLock:
            self.poolBlockNumber += 1
            self.poolRawBlock = None
            sampleBlock = self.poolSampleBlock
            self.poolSampleBlock = None
            derivedBlock = self.poolDerivedBlock
            self.poolDerivedBlock = None
            poolLineBlock = self.poolLineBlock
            self.poolLineBlock = None
        return [sampleBlock, derivedBlock, poolLineBlock]
    def GenerateDerived(self, sample):
        derived = [0.0] * len(self.dictOutputChannel)
        i = 0
        for name, formula in self.dictDerivedFormula.items():
            try:
                derived[i] = eval(formula)
            except:
                pass  # should not get here
            i += 1
        return derived
    def SetupDerived(self):
        # go flatten every formula, such that there is no variable references,
        #   but only have direct references to sample[n], all spelled out
        try:
            # map nickname to index of sample; eg dictSampleFormula['SOC_GFX_PROBE_V'] is 'sample[0]'
            dictSampleFormula = OrderedDict()
            i = 0
            for name, info in self.dictRawInputChannel.items():
                nickname = info['nickname']
                dictSampleFormula[nickname] = '(sample[' + str(i) + '])'  # parens for readability
                i += 1
            # map the derived variables' formula, in order by index;
            #   eg dictDerivedFormula[0] is formula of: derived[0]
            self.dictDerivedFormula = OrderedDict()
            for name, info in self.dictOutputChannel.items():
                self.dictDerivedFormula[name] = info['FormulaString']
            # spell out formula in terms of sample[n], with respect to dependency order
            listDependency = list(self.listDependsOnOrderByName)
            while len(listDependency)>0:
                nameDependency = listDependency.pop(0)
                formula = self.dictDerivedFormula[nameDependency]
                # replace with sample[n]
                for n, f in dictSampleFormula.items():
                    formula = formula.replace(n, f)
                # replace with derived[n]
                for n, f in self.dictDerivedFormula.items():
                    formula = formula.replace(n, f)
                # propagate forward to next more dependent formula
                self.dictDerivedFormula[nameDependency] = formula
            return True
        except:
            pass
        return False
    def GenerateDerived_SlowNotUsedKeepForReference(self, sample):
        if len(sample)!=len(self.dictRawInputChannel):
            return []  # should not get here
        dictValues = {}
        i = 0
        for name, info in self.dictRawInputChannel.items():
            nickname = info['nickname']
            dictValues[nickname] = sample[i]
            i += 1
        # generate derived, in order of dictOutputChannel
        for name in self.listDependsOnOrderByName:
            formula = self.dictOutputChannelFormula[name]
            for variable, value in dictValues.items():
                if variable in formula:
                    # parenthesis not really necessary but for readability
                    value = '(' + str(value) + ')'
                    formula = formula.replace(variable, value)
            try:
                dictValues[name] = eval(formula)
            except:
                dictValues[name] = 0.0  # should not get here
        # generate derived, in order of dictOutputChannel
        derived = [0.0] * len(self.dictOutputChannel)
        i = 0
        for name, info in self.dictOutputChannel.items():
            try:
                derived[i] = dictValues[name]
            except:
                pass  # should not get here
            i += 1
        return derived
    def ResetVipAndPlot(self, packPlotVars=None):
        lookupPlotIndex = [[None]*9 for i in range(3)]  # 3 plots, each have 9 values to plot
        if packPlotVars!=None:
            for i in range(9):
                if packPlotVars[i]=='':
                    continue
                # match to header, then get trio
                for index in range(len(self.lookupVipIndex[0])):
                    if self.lookupVipIndex[0][index]==packPlotVars[i]:
                        lookupPlotIndex[0][i] = self.lookupVipIndex[1][index]
                        lookupPlotIndex[1][i] = self.lookupVipIndex[2][index]
                        lookupPlotIndex[2][i] = self.lookupVipIndex[3][index]
                        break
            # clear data
            with self.lockVip:
                self.vipData = [None] * 5
                self.vipData[0] = list(self.lookupVipIndex[0])  # header
                for i in range(1, 5):
                    self.vipData[i] = [None] * len(self.lookupVipIndex[i])
                self.lookupPlotIndex = lookupPlotIndex
                #
                self.plotData = [[None]*9 for i in range(3)]
        return True
    def BuildVipAndPlotPack(self):
        packVip = [None] * 5
        packPlot = [[None]*9 for i in range(3)]  # 3 plots, each have 9 values
        with self.lockVip:
            packVip[0] = self.vipData[0]  # just header, no need to copy
            for i in range(1, 5):
                packVip[i] = list(self.vipData[i])
            for i in range(3):
                packPlot[i] = list(self.plotData[i])
        return [packVip, packPlot]
    def UpdateVip(self, sample, derived):
        # the fastest way to do this is to not create any new lists
        lenSample = len(sample)
        lenDerived = len(derived)
        try:
            with self.lockVip:
                for row in range(1, 5):
                    for col in range(len(self.lookupVipIndex[row])):
                        index = self.lookupVipIndex[row][col]
                        if index==None:
                            self.vipData[row][col] = 0.0
                            continue
                        if index<lenSample:
                            value = sample[index]
                        else:
                            index = index - lenSample
                            if index<lenDerived:
                                value = derived[index]
                            else:
                                value = 0.0  # should not get here
                        self.vipData[row][col] = value
                for plotIndex in range(3):
                    for setIndex in range(9):
                        index = self.lookupPlotIndex[plotIndex][setIndex]
                        if index!=None:
                            value = 0.0
                            if index<lenSample:
                                value = sample[index]
                            else:
                                index = index - lenSample
                                if index<lenDerived:
                                    value = derived[index]
                        else:
                            value = None
                        self.plotData[plotIndex][setIndex] = value
        except:
            return False
        return True
    def SetMovAvgFrame(self, movAvgFrameInMilliseconds):
        # number of samples to average within the 500 frame, given time frame
        try:
            # every 1msec is the sample rate divided by 1000
            needed = (self.sampleRate*movAvgFrameInMilliseconds)/1000.0
            needed = max(1,(min(500,int(needed))))
        except:  # covers None
            needed = 1
        with self.lockSamplesHeld:
            self.neededSamplesForMovAvg = needed
    def FlushSamplesHeld(self, cbProgress=None, \
        cbVipAndPlot=None):  # to be executed periodically
        if len(self.samplesHeld)==0:
            return False
        with self.lockSamplesHeld:
            samples = self.samplesHeld
            self.samplesHeld = []
            neededSamplesForMovAvg = self.neededSamplesForMovAvg
        try:
            if not self.usePool:
                # no don't do thread pool
                while len(samples)>0:
                    rawBlock, timestamp0 = samples.pop(0)
                    if self.trueTimestamp0==None:
                        self.trueTimestamp0 = timestamp0.replace(second=0, microsecond=0)
                    numVariables = len(rawBlock)
                    doFlush = True
                    doFlushWithOversample = False
                    lines = []
                    for i in range(len(rawBlock[0])):  # samples / row
                        sample = []
                        if not self.live:
                            for j in range(numVariables):  # variables / column
                                sample.append(rawBlock[j][i])
                            derived = self.GenerateDerived(sample)
                            # oversample
                            if self.sampleOversample!=1:
                                doFlush = False
                                if self.numSamplesFlushed%self.sampleOversample==0:
                                    oversample = list(sample)  # setup accumulation
                                else:
                                    for v in range(numVariables):
                                        oversample[v] += sample[v]
                                    if (self.numSamplesFlushed+1)%self.sampleOversample==0:
                                        for v in range(numVariables):
                                            oversample[v] /= self.sampleOversample
                                        overderived = self.GenerateDerived(oversample)
                                        doFlush = True
                                        doFlushWithOversample = True
                            # MovAvg
                            if neededSamplesForMovAvg>1:
                                flushed = self.numSamplesFlushed % 500
                                if flushed<neededSamplesForMovAvg:
                                    if flushed==0:  # first sample
                                        sampleMovAvg = list(sample)
                                        derivedMovAvg = list(derived)
                                    else:
                                        for i in range(len(sample)):
                                            sampleMovAvg[i] += sample[i]
                                        for i in range(len(derived)):
                                            derivedMovAvg[i] += derived[i]
                                        if flushed==(neededSamplesForMovAvg-1):  # ready
                                            for i in range(len(sample)):
                                                sampleMovAvg[i] /= neededSamplesForMovAvg
                                            for i in range(len(derived)):
                                                derivedMovAvg[i] /= neededSamplesForMovAvg
                            # update GUI
                            if (self.numSamplesFlushed+1)%500==0:
                                if neededSamplesForMovAvg>1:
                                    self.UpdateVip(sample=sampleMovAvg, derived=derivedMovAvg)
                                else:
                                    self.UpdateVip(sample=sample, derived=derived)
                                if cbVipAndPlot!=None:
                                    packVipAndPlot = self.BuildVipAndPlotPack()
                                    cbVipAndPlot(packVipAndPlot)
                            if (cbProgress!=None) and (self.numSamplesFlushed%100==0):
                                progress = float(self.numSamplesFlushed)
                                progress = progress / float(self.sampleCountMax)
                                progress = min(100, int(round(progress*100)))
                                cbProgress(progress)
                        else:
                            # live, 1Hz (1 sample per second)
                            for j in range(len(rawBlock)):  # variables / column
                                sample.append(rawBlock[j][i])
                            derived = self.GenerateDerived(sample)
                            #
                            self.UpdateVip(sample=sample, derived=derived)
                            if cbVipAndPlot!=None:
                                packVipAndPlot = self.BuildVipAndPlotPack()
                                cbVipAndPlot(packVipAndPlot)
                        if doFlush and (self.outputfilename!=None) and \
                            (self.numSamplesFlushed<self.sampleCountMax) and \
                            (self.numSamplesFlushed<self.hardMaxSamplesFlushed):
                            if not self.live:
                                sec = self.numSamplesFlushed / self.sampleRate
                                line = self.trueTimestamp0.strftime("%#m/%#d/%Y %H:%M") + \
                                    "," + "{0:.6g}".format(sec)
                            else:
                                line = timestamp0.strftime("%#m/%#d/%Y %H:%M") + \
                                    "," + str(self.numSamplesFlushed)  # note, 1Hz
                            if doFlushWithOversample:
                                line = line + "," + \
                                    ','.join("{0:.6g}".format(e) for e in oversample)
                                line = line + "," + \
                                    ','.join("{0:.6g}".format(e) for e in overderived)
                            else:
                                line = line + "," + \
                                    ','.join("{0:.6g}".format(e) for e in sample)
                                line = line + "," + \
                                    ','.join("{0:.6g}".format(e) for e in derived)
                            lines.append(line)
                        self.numSamplesFlushed += 1
                        if self.killStatus:
                            break
                    #
                    if lines!=[]:
                        with open(self.outputfilename, 'a') as outputfile:
                            for line in lines:
                                print(line, file=outputfile)
                        outputfile.close()
            else:
                # yes do thread pool method
                while len(samples)>0:
                    rawBlock, timestamp0 = samples.pop(0)
                    if self.trueTimestamp0==None:
                        self.trueTimestamp0 = timestamp0.replace(second=0, microsecond=0)
                    numVariables = len(rawBlock)
                    sampleBlock, derivedBlock, lineBlock = \
                        self.PoolGeneratedDerivedBlock(rawBlock, self.sampleOversample)
                    if self.killStatus:
                        break
                    # oversample
                    if self.sampleOversample!=1:
                        neededSamplesForMovAvg = 1
                        flushedDryRun = self.numSamplesFlushed
                        for index in range(500):
                            if (flushedDryRun+self.sampleOversample)<self.sampleCountMax:
                                flushedDryRun += 1
                                if index%self.sampleOversample==0:
                                    oversample = list(sampleBlock[index])  # setup accumulation
                                    oversampleIndex = index
                                    sampleBlock[index] = None
                                else:
                                    for v in range(numVariables):
                                        oversample[v] += sampleBlock[index][v]
                                    sampleBlock[index] = None
                                    if (index+1)%self.sampleOversample==0:
                                        for v in range(numVariables):
                                            oversample[v] /= self.sampleOversample
                                        overderived = self.GenerateDerived(oversample)
                                        sampleBlock[oversampleIndex] = oversample
                                        derivedBlock[oversampleIndex] = overderived
                                        #
                                        sec = self.numSamplesFlushed / self.sampleRate
                                        line = self.trueTimestamp0.strftime("%#m/%#d/%Y %H:%M") + \
                                            "," + "{0:.6g}".format(sec)
                                        line = line + "," + \
                                            ','.join("{0:.6g}".format(e) for e in oversample)
                                        line = line + "," + \
                                            ','.join("{0:.6g}".format(e) for e in overderived)
                                        lineBlock[oversampleIndex] = line
                            else:
                                lineBlock[index] = ''
                    if self.killStatus:
                        break
                    # update GUI, once per raw block
                    if neededSamplesForMovAvg>1:
                        sampleMovAvg = list(sampleBlock[0])
                        lenSample = len(sampleMovAvg)
                        for i in range(lenSample):
                            for j in range(1, neededSamplesForMovAvg):
                                sampleMovAvg[i] += sampleBlock[j][i]
                            sampleMovAvg[i] /= neededSamplesForMovAvg
                        derivedMovAvg = self.GenerateDerived(sampleMovAvg)
                        self.UpdateVip(sample=sampleMovAvg, derived=derivedMovAvg)
                    else:
                        self.UpdateVip(sample=sampleBlock[0], derived=derivedBlock[0])
                    if cbVipAndPlot!=None:
                        packVipAndPlot = self.BuildVipAndPlotPack()
                        cbVipAndPlot(packVipAndPlot)
                    if cbProgress!=None:
                        progress = float(self.numSamplesFlushed)
                        progress = progress / float(self.sampleCountMax)
                        progress = min(100, int(round(progress*100)))
                        cbProgress(progress)
                    #
                    if self.outputfilename!=None:
                        with open(self.outputfilename, 'a') as outputfile:
                            for line in lineBlock:
                                if (self.numSamplesFlushed<self.sampleCountMax) and \
                                    (self.numSamplesFlushed<self.hardMaxSamplesFlushed) and \
                                    (line!=''):
                                    print(line, file=outputfile)
                                self.numSamplesFlushed += 1
                        outputfile.close()
                        if self.killStatus:
                            break
        except:
            pass
        return True
    def Callback(self, task_handle, every_n_samples_event_type,
                 number_of_samples, callback_data):
        try:
            block = self.inTask.read(number_of_samples_per_channel=self.samplesPerChan)
            with self.lockSamplesHeld:
                self.samplesHeld.append((block, datetime.datetime.now()))
            self.numSamplesAcquired += number_of_samples
            if not self.live:
                if self.numSamplesAcquired >= self.sampleCountMax:
                    self.inTask.stop()
        except:
            pass
        return 0
    def IsSamplingAndFlushingDone(self):
        return not self.live and \
            (self.numSamplesAcquired >= self.sampleCountMax) and \
            (self.numSamplesFlushed >= self.numSamplesAcquired)
    def AverageSample(self, sample):
        for chan in range(len(sample)):
            sum = 0.0
            for i in range(self.samplesPerChan):
                sum += sample[chan][i]
            sample[chan] = sum / self.samplesPerChan
        return sample
    def StopSampling(self):
        if self.inTask==None:
            return
        try:
            self.inTask.stop()
        except:
            pass
        with self.lockSamplesHeld:
            self.samplesHeld = []
        self.killStatus = True
    def SampleOneSample(self, outputfilename, packPlotVars=None, overrideParams=None):
        self.live = False
        self.ResetVipAndPlot(packPlotVars=packPlotVars)
        if overrideParams!=None:
            sampleRate, sampleOversample, sampleCountMax = overrideParams
            self.sampleRate = sampleRate
            self.sampleOversample = sampleOversample 
            self.sampleCountMax = sampleCountMax
        self.inTask = self.SetupTask()
        if self.inTask==None:
            return False
        try:
            timestamp = datetime.datetime.now()
            samples = self.inTask.read(number_of_samples_per_channel=self.samplesPerChan)
            sample = self.AverageSample(samples)
            derived = self.GenerateDerived(sample)
            self.inTask.stop()
            self.inTask.close()
            # write to file
            if outputfilename!=None:
                headers = self.GenerateHeaders()
                with open(outputfilename, 'w') as outputfile:
                    for header in headers:
                        print(header, file=outputfile)
                    line = timestamp.strftime("%#m/%#d/%Y %H:%M") + ",0"
                    line = line + "," + ','.join(str(e) for e in sample)
                    line = line + "," + ','.join(str(e) for e in derived)
                    print(line, file=outputfile)
                outputfile.close()
            self.inTask = None
            self.UpdateVip(sample=sample, derived=derived)
            return True
        except:
            pass
        self.inTask = None
        return False

class CommandLineHandler():
    def processCommandLine(self, argv):
        showHelp = False
        for i in range(1, len(argv)):
            arg = argv[i]
            if ('/?' in arg) or ('-?' in arg):
                showHelp = True
            else:
                showHelp = False
        if showHelp:
            sys.stdout.write('Soc Validator, copyright 2019 Microsoft Xbox\n')
            sys.stdout.write('Usage: python ' + argv[0] + '    : to run the GUI version\n')
            sys.stdout.write('Usage: python ' + argv[0] + ' /? : to get help on commandline parameters\n')
        return 0

class XboxStateMachine():
    lockState = Lock()
    state = None  # state currently in, ie the function name
    #
    HDTIP = "172.29.197.245"
    xbconsole = RunXBApps.Console()
    # Discovery sequence variables
    isDiscoveryDone = False
    discoveryResult = None
    # Automation sequence variables
    isAutoDone = False
    autoResult = None
    parsedCsv = False
    listTests = []
    colCount = 0  # number of columns in test file, plus one (for 'Status')
    testCount = 0  # total number of tests
    testIndex = 0  # current test being run
    testKdError = [[]]  # list of list of KD errors, per test
    testResult = []  # list of results, per test
    # eg, '.\Runs\20190509080910\DUT1\T001-Power-DeferredParticles-87C\...
    #     ...all_36khz_1over_TDP_GFX_0p975_CPU_1p0875_SOC_1p13125_MEMP_0p85_Temp87.csv'
    # eg, '.\Runs\20190509080910\DUT1\T002-Vmin-DeferredParticles-87C\SomeFile.txt'
    testFileDirTemplate = [['.\\Runs\\', '%DATETIME%\\', 'DUT1\\'], \
        'Detailed_Report.csv', \
        ['%TNNN%-Power-%APP%-%TEMP%\\', \
        '%SAMPLEINFO%_%APP%_GFX_%GFX%_CPU_%CPU%_SOC_%SOC%_MEMP_%MEMP%_%TEMP%.csv'], \
        ['%TNNN%-Vmin-%APP%-%RAIL%-%TEMP%\\', 'SomeFile.txt']]  # 'SomeFile.txt' is a placeholder
    testFileDirRootActual = None  # rootpath, eg, '.\Runs\20190509_080910_SocValidator\DUT1\'
    testFileDirReportActual = None  # eg, '....\Detailed_Report.csv'
    testFileDirActual = [[]]  # [[T001-subdir,T001-filename],[T002-subdir,T002-filename],...
    errorValue = []
    lockTimeout = Lock()
    timeoutStarted = None
    timeoutStarted2 = None  # secondary
    #
    lockLogInfo = Lock()
    logInfoPid = [None, None, None, None]  # [KDHost, KDSRA, KDERA, DSMC]
    logInfoFilename = ['.\\kdhost', '.\\kdsra', '.\\kdera', '.\\dsmctrace.txt']
    logInfoFilePos = [0, 0, 0, 0]
    logFollow = [None, None, None, None]
    listKnownErrors = []
    def KillLogProcesses(self, moveFiles=None):
        with self.lockLogInfo:
            for i in range(4):
                try:
                    if self.logInfoPid[i]!=None:
                        xbconnect.KillTask(self.logInfoPid[i])
                        if self.logFollow[i]!=None:
                           try:
                               self.logFollow[i].close()
                           except:
                               pass
                except:
                    pass
            self.logInfoPid = [None, None, None, None]
            self.logFollow = [None, None, None, None]
        if moveFiles==None:
            self.DeleteLogFiles()
        else:
            rootpath, subdir, filename = moveFiles
            newFilenames = [rootpath+subdir+'KDHostOS.log', \
                rootpath+subdir+'KDSRA.log', \
                rootpath+subdir+'KDERA.log', \
                rootpath+subdir+'DSMCTrace.txt']
            self.MoveLogFiles(newFilenames=newFilenames)
        self.logInfoPos = [0, 0, 0, 0]
    def DeleteLogFiles(self):
        return self.MoveLogFiles(newFilenames=None)
    def MoveLogFiles(self, newFilenames):
        retValue = True
        for i in range(4):
            try:
                if (newFilenames==None)or(newFilenames[i]==None):
                    os.remove(self.logInfoFilename[i])
                else:
                    shutil.move(self.logInfoFilename[i], newFilenames[i])
            except:
                retValue = False
        return retValue
    def ShowLogsAndCheckForKnownError(self, guicomm):
        linesLogs = [None, None, None, None]
        clearLogWindow = [False, False, False, False]
        lookupColor = [guicomm.signalSetKdhostErrorColor, guicomm.signalSetKdsraErrorColor, \
            guicomm.signalSetKderaErrorColor, None]
        with self.lockLogInfo:
            for i in range(4):
                if self.logInfoPid[i]!=None:
                    try:
                        if self.logFollow[i]==None:
                            clearLogWindow[i] = True
                            self.logInfoFilePos[i] = 0
                            try:
                                self.logFollow[i] = open(self.logInfoFilename[i], 'r')
                            except:
                                self.logFollow[i] = None
                        if self.logFollow[i]!=None:
                            f = self.logFollow[i]
                            f.seek(self.logInfoFilePos[i])
                            linesLogs[i] = f.readlines()
                            self.logInfoFilePos[i] = f.tell()
                    except:
                        pass
                else:
                    clearLogWindow[i] = True
                    self.logInfoFilePos[i] = 0
                    if lookupColor[i]!=None:
                        lookupColor[i].emit(False)

        lookupClearAppend = [(guicomm.signalClearKdhost, guicomm.signalAppendKdhost), \
            (guicomm.signalClearKdsra, guicomm.signalAppendKdsra), \
            (guicomm.signalClearKdera, guicomm.signalAppendKdera), \
            (guicomm.signalClearDsmc, guicomm.signalAppendDsmc)]
        for i in range(4):
            clear, append = lookupClearAppend[i]
            if clearLogWindow[i]:
                clear.emit()
            if linesLogs[i]!=None:
                lines = linesLogs[i]
                for i in range(len(lines)):
                    # take out characters that may mess up log/CSV
                    lines[i] = lines[i].replace('\n', '').replace('\r', '').replace(',', '')
                    append.emit(lines[i])
        #
        if self.state!=None:
            if self.AddAnyKnownErrors(guicomm, linesLogs):
                return True
        return False
    def AddAnyKnownErrors(self, guicomm, linesLogs):
        if self.listKnownErrors==[]:
            return False
        if (self.testIndex<self.testCount) and \
            (len(self.testKdError[self.testIndex])<20):
            retValue = False
            lookupColor = [guicomm.signalSetKdhostErrorColor, guicomm.signalSetKdsraErrorColor, \
                guicomm.signalSetKderaErrorColor, None]
            for i in range(3):  # not checking DSMC
                haveError = False
                lines = linesLogs[i]
                if (lines==None) or (lines==[]):
                    continue
                for line in lines:
                    for ke in self.listKnownErrors:
                        if re.match(ke, line, re.S|re.I):
                            self.testKdError[self.testIndex].append(line)
                            haveError = True
                if haveError:
                    if lookupColor[i]!=None:
                        lookupColor[i].emit(True)
                    retValue = True
            return retValue
        else:
            return True
    def HasTimedOut(self, timeInMilliseconds):
        with self.lockTimeout:
            timeoutTime = self.timeoutStarted + \
                datetime.timedelta(microseconds=timeInMilliseconds*1000)
            return (datetime.datetime.now()>timeoutTime)
    def SetupTimeout(self):
        with self.lockTimeout:
            self.timeoutStarted = datetime.datetime.now()
    def HasTimedOut2(self, timeInMilliseconds):
        with self.lockTimeout:
            timeoutTime2 = self.timeoutStarted2 + \
                datetime.timedelta(microseconds=timeInMilliseconds*1000)
            return (datetime.datetime.now()>timeoutTime2)
    def SetupTimeout2(self):
        with self.lockTimeout:
            self.timeoutStarted2 = datetime.datetime.now()
    def GetState(self):
        with self.lockState:
            if self.state!=None:
                return self.state.__name__
            return 'None'
    def ClearErrors(self):
        self.errorValue = []
    def HasErrors(self):
        return (self.errorValue!=[])
    def GetErrors(self):
        return self.errorValue
    #
    def OnTick(self):
        if self.state!=None:
            return self.state()
        return False
    # Discovery sequence
    def IsDiscoveryDone(self):
        return self.isDiscoveryDone
    def ClearDiscoveryDone(self):
        self.isDiscoveryDone = False
    def GetDiscoveryResults(self):
        return self.discoveryResult
    def DoDiscoverySequence(self, guicomm, hdtip, softFusing, tether):
        with self.lockState:
            if self.state!=None:
                return False
        self.guicomm = guicomm
        self.errorValue = []
        self.isDiscoveryDone = False
        self.discoveryResult = None
        #
        try:
            hostName = socket.gethostname()
            hostIP = socket.gethostbyname(hostName)
            xbconnect.UpdateDevKitIni_HostIP(hostIP)
        except:
            pass
        #
        self.xbconsole.set_PCname(xbconnect.GetHostName())
        self.xbconsole.set_PCIpAddress(xbconnect.GetHostIP())
        ftdi = xbconnect.GetFTDI()
        self.xbconsole.set_Ftdi(ftdi)
        #
        self.xbconsole.ConsoleSoftFusing = softFusing
        self.xbconsole.HDTIP = hdtip
        if self.xbconsole.ConsoleSoftFusing:
            xbconnect.ResetSmcFlags()
            xbconnect.SetupHDTSmcFlags(tether)
        else:
            xbconnect.ResetSmcFlags()
            xbconnect.SetupNoHDTSmcFlags(tether)
        if tether:
            try:
                xbconnect.StartDevkittool(ftdi['SerialName'])
            except:
                pass
        #
        xbconnect.ResetCycle()
        self.SetupTimeout()
        self.SetupTimeout2()  # use secondary for in-between checking
        #
        try:
            pid = xbconnect.StartKdhost(self.xbconsole.PCIpAddress)
            with self.lockLogInfo:
                self.logInfoPid[0] = pid
        except:
            pass
        #
        pid = xbconnect.StartDSMCTrace(self.xbconsole.Ftdi_Serial)
        if self.xbconsole.ConsoleSoftFusing:
            cmd = "perl HDT_anubis_fuseReadModifyWrite_pmm_ver2.pl + \"protocol=yaap, ip=" + \
                self.xbconsole.HDTIP + "\""  + " -f -vid nom -soc unknown"
            os.system(cmd)
        with self.lockLogInfo:
            self.logInfoPid[3] = pid
        #
        self.consoleHostIP = None
        with self.lockState:
            self.state = self.DiscoveryWaitForResetDone
        return True
    def DiscoveryWaitForResetDone(self):
        moveToNextState = False
        if self.HasTimedOut2(5000):  # every 5 seconds, check ChkIfSRABootedNonBlocking 
            self.SetupTimeout2()
            if self.consoleHostIP==None:
                self.consoleHostIP = xbconnect.GetConsoleHostIP()
            if (self.consoleHostIP!=None) and \
                xbconnect.ChkIfSRABootedNonBlocking(self.consoleHostIP):
                moveToNextState = True
            elif self.HasTimedOut(300000):  # up to 5 minutes
                moveToNextState = True
        if moveToNextState:
            with self.lockState:
                self.state = self.DiscoverySequenceDone
        return True
    def DiscoverySequenceDone(self):
        try:
            self.xbconsole.ConsoleHostIP = xbconnect.GetConsoleHostIP()
            self.xbconsole.ConsoleSystemIP = xbconnect.GetConsoleSystemIP(self.xbconsole.ConsoleHostIP)
            try:
                pid = xbconnect.StartKdSRA(self.xbconsole.ConsoleHostIP)
                with self.lockLogInfo:
                    self.logInfoPid[1] = pid
            except:
                pass
            try:
                pid = xbconnect.StartKdERA(self.xbconsole.ConsoleHostIP)
                with self.lockLogInfo:
                    self.logInfoPid[2] = pid
            except:
                pass
        except:
            pass
        self.discoveryResult = (self.xbconsole.ConsoleHostIP, self.xbconsole.ConsoleSystemIP)
        self.isDiscoveryDone = True
        self.guicomm.signalAppendStatus.emit('Finished Xbox Discovery.')
        with self.lockState:
            self.state = None
        return True
    # Automation sequence helpers
    def AutoGetValidApps(self):
        validApps = []
        try:
            # directories under '.\Apps' (eg, '.\Apps\DeferredParticles')
            for dirname in glob.iglob('.\\Apps\\**', recursive=True):
                if not os.path.isfile(dirname):
                    if (dirname.count('\\')==2) and (dirname!='.\\Apps\\'):
                        dirname = dirname.replace('.\\Apps\\', '')
                        validApps.append(dirname)
        except:
            pass
        return validApps
    def ParseKnownErrors(self, knownErrorFilenames):
        self.listKnownErrors = []
        self.parsedKnownErrors = True
        knownErrorFilenames = knownErrorFilenames.replace(';', ',')
        filenames = knownErrorFilenames.split(',')
        for filename in filenames:
            if filename=='':
                continue
            try:
                filename = filename.strip(' \t\r\n')
                with open(filename,'r') as file:
                    lines = file.readlines()
                file.close()
                for line in lines:
                    if line.startswith('string:'):
                        line = line[7:]
                        line = line.strip(' \t\r\n')
                        self.listKnownErrors.append(line)
            except:
                self.errorValue.append('Error: Unable to parse Known Error file(s)!!')
                self.parsedKnownErrors = False
        return self.parsedKnownErrors
    def SetupTestSummary(self):
        # assumes ParseTestsCsv() already done
        if not self.parsedCsv:
            return []
        badLoc = []
        lastLocChecked = ''  # for efficiency
        for i in range(self.testCount):
            loc = self.listTests[i]['Summary File Location']
            if (loc==lastLocChecked)or(loc=='NA'):
                continue
            lastLocChecked = loc
            if not os.path.exists(loc):
                badLoc.append(loc)
                continue
            # create MasterLog if not exist, add header
            masterLog = loc.rstrip('\\') + self.masterLogFilename
            if not os.path.exists(masterLog):
                try:
                    with open(masterLog, 'w') as file:
                        print(self.logHeader, file=file)
                    file.close()
                except:
                    badLoc.append(loc)
            else:  # exists, try reading
                try:
                    with open(masterLog, 'r') as file:
                        pass
                    file.close()
                except:
                    badLoc.append(loc)
        return badLoc
    def FinalWriteTestSummaryEntry(self):
        return self.WriteTestSummaryEntry(loc=None, line=None)
    def WriteTestSummaryEntry(self, loc, line, retry=3):
        # add to backlog, then write out all together;
        # if cannot write out, hold in backlog
        if (loc!=None)and(line!=None):
            self.backlogSummary.append([loc, line])
        retValue = True
        for i in range(retry):
            if len(self.backlogSummary)==0:
                break
            retValue = True
            for pairLocLine in self.backlogSummary[:]:
                try:
                    loc, line = pairLocLine
                    logfilename = loc.rstrip('\\') + self.masterLogFilename
                    with open(logfilename, 'a') as file:
                        print(line, file=file)
                    file.close()
                    self.backlogSummary.remove(pairLocLine)
                except:
                    retValue = False
            if retValue==True:
                break
            time.sleep(1)
        return retValue
    def ParseTestsCsv(self, testFilename, tableAutoFile=None):
        """
        example rows, with header:
        Operation,App,Target Temp,GFX (mV),CPU (mV),NB/SOC (mV),MemPhy (mV),Rail to Vmin,Step Size (mV),Test Time (sec),Variable Name,Lowest VID (mV),Summary File Location,GPU-Power-Saving (Y/N),CPU-Power-Saving (Yes/No),DDR Speed
        Power,ComputeParticlesWithCRC,47,1000,1000,1000,1000,NA,NA,NA,NA,NA,NA,Yes,No,Default
        Vmin,DeferredParticles,47,1000,1100,1000,1000,CPU,12.5,10,CPURail_Vmin,750,\\xbx\projects\Anubis\Test\Summary\,No,No,Default
        """
        self.listTests = []
        self.colCount = 1
        self.testCount = 0

        validApps = self.AutoGetValidApps()
        listHeader = ['Status']
        appColIndex = -1
        self.parsedCsv = True
        try:
            with open(testFilename) as file:
                csvReader = csv.reader(file)
                for row in csvReader:
                    # only get tests after seeing the header row ('Operation', 'App', etc)
                    if self.colCount==1:
                        if 'Operation' in row:
                            listHeader = ['Status']
                            for colName in row:
                                colName = colName.strip(' \t\n\r')
                                listHeader.append(colName)
                                if colName=='App':
                                    appColIndex = self.colCount
                                self.colCount += 1
                            self.testCount = 0
                            self.listTests = []
                            #
                            if appColIndex==-1:
                                self.parsedCsv = False
                                self.errorValue.append('Error: No App column!!')
                                break
                    elif (len(row)+1)==self.colCount:
                        dictInfo = OrderedDict()
                        colIndex = 1
                        for colValue in row:
                            colName = listHeader[colIndex]
                            dictInfo[colName] = colValue
                            if colIndex==appColIndex:
                                appToRun = colValue
                            colIndex += 1
                        if appToRun not in validApps:
                            self.parsedCsv = False
                            self.errorValue.append('Error: App (' + appToRun + ') is not ' + \
                                'in ..\\Apps directory (check uppercase/lowercase)!!')
                            break
                        self.listTests.append(dictInfo)
                        self.testCount += 1
                    else:
                        self.errorValue.append('Error: Bad number of columns in test number ' + \
                            str(self.testCount+1) + '!!')
                        break
            file.close()
            if self.testCount==0:
                self.parsedCsv = False
                self.errorValue.append('Error: No valid tests!!')
        except:
            self.errorValue.append('Error: Unable to parse CSV file!!')
            self.parsedCsv = False
        # populate table
        if tableAutoFile!=None:
            tableAutoFile.clear()
            if self.parsedCsv:
                tableAutoFile.setRowCount(self.testCount)
                tableAutoFile.setColumnCount(self.colCount)
                tableAutoFile.setHorizontalHeaderLabels(listHeader)
                for row in range(self.testCount):
                    dictInfo = self.listTests[row]
                    col = 1
                    for value in dictInfo.values():
                        tableAutoFile.setItem(row, col, QTableWidgetItem(value))
                        col += 1
        #
        if self.parsedCsv:
            self.testKdError = [[] for i in range(self.testCount)]
            self.testResult = [None] * self.testCount
        else:
            self.testKdError = [[]]
            self.testResult = []
        return self.parsedCsv
    # Automation sequence
    def IsAutoDone(self):
        return self.isAutoDone
    def ClearAutoDone(self):
        self.isAutoDone = False
    def GetAutoResults(self):
        return self.autoResult
    def AutoReplaceMacroDatetime(self, value, macroDatetime):
        return self.AutoReplaceMacro(value, macroDatetime)
    def AutoReplaceMacro(self, value, macroDatetime, \
        macroTestNumber=None, macroApp=None, \
        macroRail=None, macroTemp=None, \
        macroSampleInfo=None, macroGfx=None, macroCpu=None, macroSoc=None, macroMemp=None):
        value = value.replace('%DATETIME%', macroDatetime)
        if macroTestNumber!=None:
            value = value.replace('%TNNN%', macroTestNumber)
        if macroApp!=None:
            value = value.replace('%APP%', macroApp)
        if macroRail!=None:
            value = value.replace('%RAIL%', macroRail)
        if macroTemp!=None:
            value = value.replace('%TEMP%', macroTemp)
        if macroSampleInfo!=None:
            value = value.replace('%SAMPLEINFO%', macroSampleInfo)
        if macroGfx!=None:
            macroGfx = str(macroGfx).replace('.', 'p')  # note, is float
            value = value.replace('%GFX%', macroGfx)
        if macroCpu!=None:
            macroCpu = str(macroCpu).replace('.', 'p')  # note, is float
            value = value.replace('%CPU%', macroCpu)
        if macroSoc!=None:
            macroSoc = str(macroSoc).replace('.', 'p')  # note, is float
            value = value.replace('%SOC%', macroSoc)
        if macroMemp!=None:
            macroMemp = str(macroMemp).replace('.', 'p')  # note, is float
            value = value.replace('%MEMP%', macroMemp)
        return value
    def AutoGetTestFilename(self, testIndex=-1):
        # returns [rootpath, subdir, filename]
        # if testIndex<0, then just build path up to the actual test
        now = datetime.datetime.now()
        macroDatetime = now.strftime("%Y%m%d%H%M%S")  # eg, '20190509080910', aka 'Job ID'
        # root path, create if need to
        rootpath = self.testFileDirRootActual
        if rootpath==None:
            subdirs = self.testFileDirTemplate[0]
            rootpath = ''
            try:
                for subdir in subdirs:
                    subdir = self.AutoReplaceMacroDatetime(subdir, macroDatetime)
                    rootpath = rootpath + subdir
                    if not os.path.exists(rootpath):
                        os.mkdir(rootpath)
                self.testFileDirRootActual = rootpath
                self.testFileDirReportActual = rootpath + self.testFileDirTemplate[1]
                self.testFileDirActual = [None] * self.testCount
                self.UpdateResultFile(justWriteHeader=True)
            except:
                return None
        # test subdirectory and filename, which depends on Power/Vmin, go create if need to
        if (testIndex>=0) and (testIndex<self.testCount):
            dictTest = self.listTests[self.testIndex]
            macroTestNumber = "T{:03d}".format(testIndex+1)
            macroApp = dictTest['App']
            macroRail = dictTest['Rail to Vmin']
            macroTemp = 'Temp' + dictTest['Target Temp']
            macroSampleInfo = self.testInfo[4]  # eg, 'all_36khz_1over'
            try:
                macroGfx, macroCpu, macroSoc, macroMemp = self.testInfo[5]
                macroGfx = macroGfx / 1000.0
                macroCpu = macroCpu / 1000.0
                macroSoc = macroSoc / 1000.0
                macroMemp = macroMemp / 1000.0
            except:
                macroGfx = None
                macroCpu = None
                macroSoc = None
                macroMemp = None
            operation = dictTest['Operation']
            if operation=='Power':
                subdir, filename = self.testFileDirTemplate[2]
            elif operation=='Vmin':
                subdir, filename = self.testFileDirTemplate[3]
            else:  # should not get here
                return None
            subdir = self.AutoReplaceMacro(subdir, macroDatetime=macroDatetime, \
                macroTestNumber=macroTestNumber, macroApp=macroApp, \
                macroRail=macroRail, macroTemp=macroTemp, macroSampleInfo=macroSampleInfo, \
                macroGfx=macroGfx, macroCpu=macroCpu, macroSoc=macroSoc, macroMemp=macroMemp)
            filename = self.AutoReplaceMacro(filename, macroDatetime=macroDatetime, \
                macroTestNumber=macroTestNumber, macroApp=macroApp, \
                macroRail=macroRail, macroTemp=macroTemp, macroSampleInfo=macroSampleInfo, \
                macroGfx=macroGfx, macroCpu=macroCpu, macroSoc=macroSoc, macroMemp=macroMemp)
            testdir = rootpath + subdir
            if not os.path.exists(testdir):
                os.mkdir(testdir)
            self.testFileDirActual[testIndex] = [subdir, filename]
            return [rootpath, subdir, filename]
        return None

    def DoAutoSequence(self, guicomm, nidaqHandler, configFilename, boardType, \
        testFilename, tableAutoFile, knownErrorFilenames, tec, autoOneSample, \
        packInfoTemp, autoSkipTemp, hdtip, softFusing, tether, usePool):
        with self.lockState:
            if self.state!=None:
                return False
        if not self.ParseKnownErrors(knownErrorFilenames):
            return False
        self.guicomm = guicomm
        xbconnect.KillAllLogTasks()
        xbconnect.KillDevkittoolTask()
        self.KillLogProcesses()
        self.nidaqHandler = nidaqHandler
        if not self.nidaqHandler.ParseNidaqXml(filename=configFilename):
            return False
        self.tableAutoFile = tableAutoFile
        self.guicomm.signalProgressAuto.emit(0)
        self.autoBoardType = boardType
        self.textStatusPrefix = 'Automation: '
        self.errorValue = []
        self.isAutoDone = False
        self.autoResult = None
        self.vidVoltages = None
        self.tec = tec
        self.autoVariableNames = None  # GFX, CPU, SOC, MemPhy
        self.autoOneSample = autoOneSample
        self.infoTemp, self.infoTempAutoAdjust, self.timeBetweenTempAdjustsInSeconds, \
            self.tempStableRange, self.tempAdjustRange, self.tempStableCountNeeded = \
            packInfoTemp
        self.autoSkipTemp = autoSkipTemp
        self.autoUsePool = usePool
        #
        self.xbconsole.ConsoleSoftFusing = softFusing
        self.xbconsole.HDTIP = hdtip
        self.tether = tether
        #
        self.testIndex = 0
        if not self.ParseTestsCsv(testFilename, tableAutoFile):
            return False
        # [startTime, endTime, actualTemp, hostName, 'all_36khz_1over', [GFX,CPU,SOC,MEMP]]
        self.testInfo = [None] * 6
        self.testInfo[3] = xbconnect.GetHostName()
        self.testInfo[4] = self.nidaqHandler.projectName.lower()
        self.testInfo[4] = self.testInfo[4].replace('sample.pjdaq', '')  # eg, 'all_36khz_1over'
        self.testInfo[5] = [None] * 4
        self.jtagId = None
        # note, everything before 'Test Date' is directly from test CSV file
        self.logHeader = 'Operation,App,Target Temp,GFX (mV),CPU (mV),' + \
            'NB/SOC (mV),MemPhy (mV),Rail to Vmin,Step Size (mV),Test Time (sec),' + \
            'Variable Name,Lowest VID (mV),Test Date,Test Start,Test End Time,' + \
            'JTAG ID,Host PC Name,PCBA SN,Fused VID,Max Junction Temp,' + \
            'Job ID,Vmin,Status,Keyword Found'
        self.masterLogFilename = '\\Master.log'
        badLoc = self.SetupTestSummary()
        if badLoc!=[]:
            self.guicomm.signalAppendStatus.emit( \
                'Unable to access these Summary location(s):')
            for loc in badLoc:
                self.guicomm.signalAppendStatus.emit(loc)
            return False
        self.backlogSummary = []
        #
        self.testFileDirRootActual = None
        self.testFileDirReportActual = None
        self.testFileDirActual = [None] * self.testCount
        #
        with self.lockState:
            self.state = self.AutoSetupNextTest
        return True
    def AutoSetupNextTest(self):
        self.textStatusPrefix = 'Automation (test ' + str(self.testIndex+1) + \
            ' of ' + str(self.testCount) + '): '
        self.tableAutoFile.setItem(self.testIndex, 0, QTableWidgetItem('In Progress'))
        self.testInfo[0] = datetime.datetime.now()
        self.testInfo[2] = None  # clear Max Junction Temp
        self.moveFiles = self.AutoGetTestFilename(testIndex=self.testIndex)
        #
        self.xbconsole.set_PCname(xbconnect.GetHostName())
        self.xbconsole.set_PCIpAddress(xbconnect.GetHostIP())
        ftdi = xbconnect.GetFTDI()
        self.xbconsole.set_Ftdi(ftdi)
        if self.xbconsole.ConsoleSoftFusing:
            xbconnect.ResetSmcFlags()
            xbconnect.SetupHDTSmcFlags(self.tether)
        else:
            xbconnect.ResetSmcFlags()
            xbconnect.SetupNoHDTSmcFlags(self.tether)
        if self.tether:
            try:
                xbconnect.StartDevkittool(ftdi['SerialName'])
            except:
                pass
            self.tether = False  # only first time
        #
        self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
            'Reset Xbox console.')
        xbconnect.ResetCycle()
        self.SetupTimeout()
        self.SetupTimeout2()  # use secondary for in-between checking
        #
        try:
            pid = xbconnect.StartKdhost(self.xbconsole.PCIpAddress)
            with self.lockLogInfo:
                self.logInfoPid[0] = pid
        except:
            pass
        #
        pid = xbconnect.StartDSMCTrace(self.xbconsole.Ftdi_Serial)
        with self.lockLogInfo:
            self.logInfoPid[3] = pid
        if self.xbconsole.ConsoleSoftFusing:
            cmd = "perl HDT_anubis_fuseReadModifyWrite_pmm_ver2.pl + \"protocol=yaap, ip=" + \
                self.xbconsole.HDTIP + "\""  + " -f -vid nom -soc unknown"
            os.system(cmd)
        #
        self.consoleHostIP = None
        with self.lockState:
            self.state = self.AutoWaitForResetDoneThenDeployApp
        return True
    def AutoWaitForResetDoneThenDeployApp(self):
        moveToNextState = False
        if self.HasTimedOut2(5000):  # every 5 seconds, check ChkIfSRABootedNonBlocking 
            self.SetupTimeout2()
            if self.consoleHostIP==None:
                self.consoleHostIP = xbconnect.GetConsoleHostIP()
            if (self.consoleHostIP!=None) and \
                xbconnect.ChkIfSRABootedNonBlocking(self.consoleHostIP):
                moveToNextState = True
            elif self.HasTimedOut(300000):  # up to 5 minutes
                moveToNextState = True
        if moveToNextState:
            if self.jtagId==None:
                try:
                    self.jtagId = str(xbconnect.GetJTAGID())
                except:
                    pass
            try:
                self.xbconsole.ConsoleHostIP = xbconnect.GetConsoleHostIP()
                self.xbconsole.ConsoleSystemIP = xbconnect.GetConsoleSystemIP(self.xbconsole.ConsoleHostIP)
                self.discoveryResult = (self.xbconsole.ConsoleHostIP, self.xbconsole.ConsoleSystemIP)
                try:
                    pid = xbconnect.StartKdSRA(self.xbconsole.ConsoleHostIP)
                    with self.lockLogInfo:
                        self.logInfoPid[1] = pid
                except:
                    pass
                try:
                    pid = xbconnect.StartKdERA(self.xbconsole.ConsoleHostIP)
                    with self.lockLogInfo:
                        self.logInfoPid[2] = pid
                except:
                    pass
                self.ShowLogsAndCheckForKnownError(guicomm=self.guicomm)  # nudge GUI
            except:
                pass
            #
            if self.vidVoltages==None:
                self.vidVoltages = [1000.0, 1000.0, 1000.0, 1000.0]
                try:
                    self.Vregobj = Vregscontrol.VRegs()
                    self.Vregobj.ftdiserial = self.xbconsole.Ftdi_Serial
                    self.Vregobj.boardtype = self.autoBoardType
                    #
                    self.vidVoltages[0] = float(self.Vregobj.readvoltage("GFX"))*1000.0
                    self.vidVoltages[1] = float(self.Vregobj.readvoltage("CPU"))*1000.0
                    self.vidVoltages[2] = float(self.Vregobj.readvoltage("SOC"))*1000.0
                    self.vidVoltages[3] = float(self.Vregobj.readvoltage("MEMPHY"))*1000.0
                    #
                    self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
                        'Got GFX_Fused_VID/CPU_Fused_VID/SOC_Fused_VID/MEMPHY_Fused_VID voltages as: ' + \
                        str(self.vidVoltages).strip('[').strip(']').replace(', ', '/') + ' mV.')
                except:
                    self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
                        'Failed to get GFX_Fused_VID/CPU_Fused_VID/SOC_Fused_VID/MEMPHY_Fused_VID voltages (' + \
                        str(self.vidVoltages).strip('[').strip(']') + ').')
                    self.errorValue.append('Failed to get voltages (' + str(self.vidVoltages).strip('[').strip(']') + ')!!')
                self.autoVariableNames = list(self.vidVoltages)
            self.ShowLogsAndCheckForKnownError(guicomm=self.guicomm)  # nudge GUI
            #
            dictTest = self.listTests[self.testIndex]
            app = dictTest['App']
            try:
                self.xbconsole.XbAppDeploy(app)
                self.appInfo = (app, \
                    self.xbconsole.ConsoleDepPackageName, \
                    self.xbconsole.ConsoleDepPackageID)
                self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
                    'Deployed Xbox app (' + app + ').')
                self.SetupTimeout()
                with self.lockState:
                    self.state = self.AutoWaitForDeployDoneThenLaunchApp
                return True
            except:
                self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
                    'Error in deploying Xbox app!!')
                self.isAutoDone = True
                with self.lockState:
                    self.state = None
        return True
    def AutoWaitForDeployDoneThenLaunchApp(self):
        if self.HasTimedOut(10000):
            dictTest = self.listTests[self.testIndex]
            app = dictTest['App']
            try:
                threading.Thread(target=self.xbconsole.XbApplaunch).start()
                self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
                    'Launched Xbox app (' + app + ').')
                self.SetupTimeout()
                with self.lockState:
                    self.state = self.AutoWaitForLaunchDoneThenSetupVoltages
            except:
                self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
                    'Error in launching Xbox app!!')
                self.isAutoDone = True
                with self.lockState:
                    self.state = None
        return True
    def AutoWaitForLaunchDoneThenSetupVoltages(self):
        if not self.HasTimedOut(20000):
            return True
        # note, both Vmin and Power will go thru this state (both once per Operation)
        #   but Vmin will go thru AutoVminAdjustVoltages multiple times as needed
        dictTest = self.listTests[self.testIndex]
        voltages = list(self.vidVoltages)  # figure out voltages to set, assume same as VID
        try:
            self.Vregobj = Vregscontrol.VRegs()
            self.Vregobj.ftdiserial = self.xbconsole.Ftdi_Serial
            self.Vregobj.boardtype = self.autoBoardType
            #
            value = dictTest['GFX (mV)']
            if '_VID' not in value:
                if '_Vmin' in value:
                    voltages[0] = self.autoVariableNames[0]
                else:
                    voltages[0] = float(value)
            self.Vregobj.setvoltage("GFX", "dsmcdbg", voltages[0])
            #
            value = dictTest['CPU (mV)']
            if '_VID' not in value:
                if '_Vmin' in value:
                    voltages[1] = self.autoVariableNames[1]
                else:
                    voltages[1] = float(value)
            self.Vregobj.setvoltage("CPU", "dsmcdbg", voltages[1])
            #
            value = dictTest['NB/SOC (mV)']
            if '_VID' not in value:
                if '_Vmin' in value:
                    voltages[2] = self.autoVariableNames[2]
                else:
                    voltages[2] = float(value)
            self.Vregobj.setvoltage("SOC", "dsmcdbg", voltages[2])
            #
            value = dictTest['MemPhy (mV)']
            if '_VID' not in value:
                if '_Vmin' in value:
                    voltages[3] = self.autoVariableNames[3]
                else:
                    voltages[3] = float(value)
            self.Vregobj.setvoltage("MEMPHY", "xbvregs", voltages[3])
            #
            self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
                'Set GFX/CPU/SOC/MEMPHY voltages to ' + \
                str(voltages).strip('[').strip(']').replace(', ', '/') + ' mV.')
        except:
            self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
                'Failed to set voltages (' + str(voltages).strip('[').strip(']') + ').')
        self.testInfo[5] = list(voltages)
        #
        self.tempAtStepFinal = None
        if not self.autoSkipTemp:
            # note, infoTemp is
            #   [tecTarget, dieTarget, tecActual, dieActual, tecReadFails, dieReadFails]
            dieTarget = float(dictTest['Target Temp'])
            dieTarget = min(max(15.0, dieTarget), 100.0)  # sanity
            self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
                'Reaching for target temperature (' + str(dieTarget) + 'C)...')
            self.infoTemp[1] = dieTarget  # dieTarget
            self.guicomm.signalClearDieTempAutoAdjust.emit()
            # note, infoTempAutoAdjust is
            #   [autoAdjust, stopWhenStable, stopWhenStableCounter]
            self.infoTempAutoAdjust[0] = True
            self.infoTempAutoAdjust[1] = True
            self.infoTempAutoAdjust[2] = 0
            #
            self.SetupTimeout2()  # use secondary to exit temperature adjusting loop
        #
        operation = dictTest['Operation']
        moveToNextTestOnError = False
        self.vminAtStepFinal = None
        self.vminRail = None
        if operation=='Vmin':
            self.testResult[self.testIndex] = 'Never Pass'
            # if Vmin, setup at/step/final voltages
            step = float(dictTest['Step Size (mV)'])
            final = float(dictTest['Lowest VID (mV)'])
            self.vminRail = dictTest['Rail to Vmin']
            if self.vminRail=='GFX':
                self.vminAtStepFinal = [voltages[0], step, final]
            elif self.vminRail=='CPU':
                self.vminAtStepFinal = [voltages[1], step, final]
            elif self.vminRail=='SOC':
                self.vminAtStepFinal = [voltages[2], step, final]
            elif self.vminRail=='MEMPHY':
                self.vminAtStepFinal = [voltages[3], step, final]
            else:  # should not get here
                moveToNextTestOnError = True
                self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
                    'Skipping test due to unknown Rail parameter (' + self.vminRail + ').')
            #
            value = dictTest['Test Time (sec)']
            try:
                self.vminTestTimeInMilliseconds = max(10, int(value))
                self.vminTestTimeInMilliseconds = min(3600, self.vminTestTimeInMilliseconds)
                self.vminTestTimeInMilliseconds *= 1000
            except:
                self.vminTestTimeInMilliseconds = 60000
            self.SetupTimeout()
            with self.lockState:
                if self.autoSkipTemp:
                    self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
                        'Skipping temperature requirements...')
                    self.state = self.AutoVminWaitForTestTime
                else:
                    self.state = self.AutoWaitForTempDone
        elif operation=='Power':
            self.testResult[self.testIndex] = 'Always Pass'
            # if Power, just need to set voltages, already done above
            self.SetupTimeout()
            with self.lockState:
                if self.autoSkipTemp:
                    self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
                        'Skipping temperature requirements...')
                    self.state = self.AutoPowerSetupMeasurement
                else:
                    self.state = self.AutoWaitForTempDone
        else:  # should not get here
            self.testResult[self.testIndex] = 'NA'
            self.tableAutoFile.setItem(self.testIndex, 0, QTableWidgetItem('NA'))
            moveToNextTestOnError = True
            self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
                'Skipping test due to unknown Operation (' + operation + ').')
        if moveToNextTestOnError:
            with self.lockState:
                self.state = self.AutoSetupNextTest
        return True
    def AutoWaitForTempDone(self):
        moveToNextState = False
        if self.HasTimedOut(timeInMilliseconds=self.timeBetweenTempAdjustsInSeconds*1000):
            self.SetupTimeout()
            try:  # note, dieActual may come back None if Xbox crashes, then move on
                tecTarget, dieTarget, tecActual, dieActual, \
                    tecReadFails, dieReadFails = self.infoTemp
                #
                adjustTec = (dieTarget-dieActual)/2.0
                if adjustTec>0:
                    adjustTec = min(adjustTec, 10.0)
                else:
                    adjustTec = max(adjustTec, -10.0)
                # only adjust TEC if big enough to bother adjusting TEC
                if (adjustTec<-self.tempAdjustRange)or(adjustTec>self.tempAdjustRange):
                    tecTarget += adjustTec
                    tecTarget = min(max(tecTarget, 15.0), 100.0)  # sanity
                    tecTarget = round(tecTarget, 1)  # must round to 1 digit to match TEC display
                    self.infoTemp[0] = tecTarget
                    #
                    self.guicomm.signalPackageTempTarget.emit(tecTarget)
                    self.tec.SetTemp(tecTarget)
                # if need to stop AutoAdjust: check if stable, using counter
                if self.infoTempAutoAdjust[1]:
                    if (adjustTec<self.tempStableRange)and(adjustTec>-self.tempStableRange):
                        self.infoTempAutoAdjust[2] += 1
                        if self.infoTempAutoAdjust[2]>self.tempStableCountNeeded:
                            self.guicomm.signalClearDieTempAutoAdjust.emit()
                            self.infoTempAutoAdjust[0] = False
                            self.infoTempAutoAdjust[2] = 0
                            moveToNextState = True  # one of two ways out
                            self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
                                'Target temperature (' + str(dieTarget) + 'C) has been reached.')
                    else:
                        self.infoTempAutoAdjust[2] = 0
                # note, check secondary inside of primary to avoid busy looping
                if self.HasTimedOut2(timeInMilliseconds=3*60*1000):  # 3 minutes
                    self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
                        'Target temperature (' + str(dieTarget) + 'C) was NOT reached, ' + \
                        'continuing with test after 3 minutes.')
                    moveToNextState = True
            except:
                moveToNextState = True
        if moveToNextState:
            dictTest = self.listTests[self.testIndex]
            with self.lockState:
                if dictTest['Operation']=='Power':
                    self.state = self.AutoPowerSetupMeasurement
                else:
                    self.state = self.AutoVminWaitForTestTime
        return True
    def AutoPowerSetupMeasurement(self):
        if self.autoOneSample:
            if not self.nidaqHandler.SampleOneSample(outputfilename='.\\output.csv'):
                self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
                    'Failed to start NIDaq measurement with ONE SAMPLE option!!')
                with self.lockState:
                    self.state = None
            else:
                self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
                    'Started and finished NIDaq measurement with ONE SAMPLE option.')
                with self.lockState:
                    self.state = self.AutoDoneWithCurrentTest
            return True
        self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
            'Starting NIDaq measurement...')
        if not self.nidaqHandler.StartSampling(outputfilename='.\\output.csv', \
            usePool=self.autoUsePool):
            self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
                'Failed to start NIDaq measurement!!')
            with self.lockState:
                self.state = None
        else:
            with self.lockState:
                self.state = self.AutoPowerWaitForMeasurementDone
        return True
    def AutoPowerWaitForMeasurementDone(self):
        self.nidaqHandler.FlushSamplesHeld(cbProgress=None, cbVipAndPlot=None)
        if self.nidaqHandler.IsSamplingAndFlushingDone():
            self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
                'Finished NIDaq measurement.')
            self.ShowLogsAndCheckForKnownError(guicomm=self.guicomm)  # nudge GUI
            # for injecting a simulated error, during debugging sessions
            injectSimulatedError = False
            if injectSimulatedError:
                self.testKdError[self.testIndex].append('User injected this simulated Power error')
            if self.testKdError[self.testIndex]!=[]:
                errors = self.testKdError[self.testIndex]
                for i in range(min(3, len(errors))):  # show up to first 3 errors
                    self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
                        'Power, error #' + str(i+1) + ', detected: ' + errors[i])
                self.testResult[self.testIndex] = 'Never Pass'
            with self.lockState:
                self.state = self.AutoDoneWithCurrentTest
        elif self.nidaqHandler.killStatus:
            self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
                'Killed at user\'s request!!')
            with self.lockState:
                self.state = None
        # set Max Junction Temp to dieTemp
        dieActual = self.infoTemp[3]
        if dieActual!=None:
            if self.testInfo[2]!=None:
                if dieActual>self.testInfo[2]:
                    self.testInfo[2] = dieActual
            else:
                self.testInfo[2] = dieActual
        return True
    def AutoVminAdjustVoltages(self):
        # set Max Junction Temp to dieTemp
        dieActual = self.infoTemp[3]
        if dieActual!=None:
            if self.testInfo[2]!=None:
                if dieActual>self.testInfo[2]:
                    self.testInfo[2] = dieActual
            else:
                self.testInfo[2] = dieActual
        # note, for Vmin only on secondary passes
        at, step, final = self.vminAtStepFinal
        if at<=final:
            self.testResult[self.testIndex] = 'Always Pass'
            # done looking for Vmin
            with self.lockState:
                self.state = self.AutoDoneWithCurrentTest
            return True
        else:
            self.testResult[self.testIndex] = 'Found Vmin'
        at = at - step
        if at<final:
            at = final
        self.vminAtStepFinal = [at, step, final]

        if self.vminRail=='GFX':
            self.Vregobj.setvoltage("GFX", "dsmcdbg", at)
            self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
                'Set Rails GFX voltage to ' + str(at) + ' mV.')
        elif self.vminRail=='CPU':
            self.Vregobj.setvoltage("CPU", "dsmcdbg", at)
            self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
                'Set Rails CPU voltage to ' + str(at) + ' mV.')
        elif self.vminRail=='SOC':
            self.Vregobj.setvoltage("SOC", "dsmcdbg", at)
            self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
                'Set Rails SOC voltage to ' + str(at) + ' mV.')
        elif self.vminRail=='MEMPHY':
            self.Vregobj.setvoltage("MEMPHY", "xbvregs", at)
            self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
                'Set Rails MEMPHY voltage to ' + str(at) + ' mV.')
        else:  # should not get here
            pass

        dictTest = self.listTests[self.testIndex]
        value = dictTest['Test Time (sec)']
        try:
            self.vminTestTimeInMilliseconds = max(10, int(value))
            self.vminTestTimeInMilliseconds = min(3600, self.vminTestTimeInMilliseconds)
            self.vminTestTimeInMilliseconds *= 1000
        except:
            self.vminTestTimeInMilliseconds = 60000
        self.SetupTimeout()
        with self.lockState:
            self.state = self.AutoVminWaitForTestTime
        return True
    def AutoVminWaitForTestTime(self):
        # for injecting a simulated error, during debugging sessions
        injectSimulatedError = False
        if injectSimulatedError:
            self.testKdError[self.testIndex].append('User injected this simulated Vmin error')
        # if no KD errors at timeout, then update Vmin value, go to AutoVminAdjustVoltages
        if self.testKdError[self.testIndex]!=[]:
            # if have KD errors before timeout, then go to AutoDoneWithCurrentTest
            errors = self.testKdError[self.testIndex]
            for i in range(min(3, len(errors))):  # show up to first 3 errors
                self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
                    'Vmin, error #' + str(i+1) + ', detected: ' + errors[i])
            # KD files to be saved as 'TNNN-...' in appropriate directory
            self.KillLogProcesses(moveFiles=self.moveFiles)
            with self.lockState:
                self.state = self.AutoDoneWithCurrentTest
        elif self.HasTimedOut(self.vminTestTimeInMilliseconds):
            # check heartbeat at end of Test Time period; ping Xbox Host IP
            if os.system('ping -n 1 '+self.discoveryResult[0])!=0:
                self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
                    'Vmin, heartbeat failure detected')
                self.testKdError[self.testIndex].append('Heartbeat failure detected')
                # KD files to be saved as 'TNNN-...' in appropriate directory
                self.KillLogProcesses(moveFiles=self.moveFiles)
                with self.lockState:
                    self.state = self.AutoDoneWithCurrentTest
                return True
            # no KD errors, update new Vmin value, and continue with Vmin adjusting
            at, step, final = self.vminAtStepFinal
            if at==final:
                self.testResult[self.testIndex] = 'Always Pass'
            if self.vminRail=='GFX':
                self.autoVariableNames[0] = at
            elif self.vminRail=='CPU':
                self.autoVariableNames[1] = at
            elif self.vminRail=='SOC':
                self.autoVariableNames[2] = at
            elif self.vminRail=='MEMPHY':
                self.autoVariableNames[3] = at
            else:  # should not get here
                pass
            with self.lockState:
                self.state = self.AutoVminAdjustVoltages
        return True
    def AutoDoneWithCurrentTest(self):
        self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
            'GFXRail_Vmin/CPURail_Vmin/SOCRail_Vmin/MEMPHYRail_Vmin values are: ' + \
            str(self.autoVariableNames).strip('[').strip(']').replace(', ', '/') + ' mV.')
        self.guicomm.signalAppendStatus.emit(self.textStatusPrefix + \
            'RESULT is ' + self.testResult[self.testIndex] + '.')
        # KD files to be saved as 'TNNN-...' in appropriate directory
        self.KillLogProcesses(moveFiles=self.moveFiles)
        dictTest = self.listTests[self.testIndex]
        if dictTest['Operation']=='Power':  # move NIDaq output file too
            self.moveFiles = self.AutoGetTestFilename(testIndex=self.testIndex)  # update this
            rootpath, subdir, filename = self.moveFiles
            try:
                shutil.move('.\Output.csv', rootpath+subdir+filename)
            except:
                pass
        #
        self.tableAutoFile.setItem(self.testIndex, 0, \
            QTableWidgetItem(self.testResult[self.testIndex]))
        self.testInfo[1] = datetime.datetime.now()
        self.UpdateResultFile()
        #
        self.testIndex += 1
        self.guicomm.signalProgressAuto.emit(min(99,int(100*self.testIndex/self.testCount)))
        if self.testIndex>=self.testCount:
            with self.lockState:
                self.state = self.AutoSequenceDone
        else:
            with self.lockState:
                self.state = self.AutoSetupNextTest
        return True
    def AutoSequenceDone(self):
        self.isAutoDone = True
        self.guicomm.signalProgressAuto.emit(100)
        self.guicomm.signalAppendStatus.emit('Finished Automation test.')
        # dump out backlog after final try
        self.FinalWriteTestSummaryEntry()
        if len(self.backlogSummary)>0:
            self.guicomm.signalAppendStatus.emit( \
                'Error: Unable to write to logs, please fix manually:')
            for loc, line in self.backlogSummary:
                self.guicomm.signalAppendStatus.emit( \
                    'Failed to write to log file: ' + loc.rstrip('\\') + \
                    self.masterLogFilename)
                self.guicomm.signalAppendStatus.emit(' this line: ' + line)
        with self.lockState:
            self.state = None
        return True
    def UpdateResultFile(self, justWriteHeader=False):
        outputfilename = self.testFileDirReportActual
        if justWriteHeader:  # write to results file, with header
            try:
                with open(outputfilename, 'w') as outputfile:
                    print(self.logHeader, file=outputfile)
                outputfile.close()
            except:
                return False
        else:  # append to results file, with result of current test
            try:
                with open(outputfilename, 'a') as outputfile:
                    dictTest = self.listTests[self.testIndex]
                    line = dictTest['Operation'] + ","
                    line += dictTest['App'] + ","
                    line += dictTest['Target Temp'] + ","
                    line += dictTest['GFX (mV)'] + ","
                    line += dictTest['CPU (mV)'] + ","
                    line += dictTest['NB/SOC (mV)'] + ","
                    line += dictTest['MemPhy (mV)'] + ","
                    line += dictTest['Rail to Vmin'] + ","
                    line += dictTest['Step Size (mV)'] + ","
                    line += dictTest['Test Time (sec)'] + ","
                    line += dictTest['Variable Name'] + ","
                    line += dictTest['Lowest VID (mV)'] + ","
                    # note, everything before 'Test Date' is directly from test CSV file
                    # Test Date
                    line += self.testInfo[0].strftime("%#m/%#d/%Y") + ","
                    # Test Start
                    line += self.testInfo[0].strftime("%H:%M:%S") + ","
                    # Test End Time
                    line += self.testInfo[1].strftime("%#m/%#d/%Y %H:%M:%S") + ","
                    # JTAG ID
                    if self.jtagId!=None:
                        line += self.jtagId + ","
                    else:
                        line += 'NA,'
                    # Host PC Name
                    if self.testInfo[3]!=None:
                        line += self.testInfo[3] + ","
                    else:
                        line += 'NA,'
                    # PCBA SN
                    line += 'NA,'
                    # Fused VID
                    line += 'NA,'
                    # Max Junction Temp
                    if self.testInfo[2]!=None:
                        line += str(round(self.testInfo[2],2)) + ","
                    else:
                        line += 'NA,'
                    # Job ID, eg 20190610144012
                    line += self.testInfo[0].strftime("%Y%m%d%H%M%S") + ","
                    # Vmin
                    if self.vminRail=='GFX':
                        vminValue = self.testInfo[5][0]
                    elif self.vminRail=='CPU':
                        vminValue = self.testInfo[5][1]
                    elif self.vminRail=='SOC':
                        vminValue = self.testInfo[5][2]
                    elif self.vminRail=='MEMPHY':
                        vminValue = self.testInfo[5][3]
                    else:
                        vminValue = None
                    if vminValue!=None:
                        line += str(int(vminValue)) + ","
                    else:
                        line += 'NA,'
                    # Status
                    line += self.testResult[self.testIndex] + ","
                    # Keyword Found
                    if self.testKdError[self.testIndex]!=[]:
                        firstError = self.testKdError[self.testIndex][0]
                        firstError = firstError.replace(',', ';')  # avoid commas in CSV file
                        line += firstError
                    else:
                        line += 'NA'
                    print(line, file=outputfile)
                    # write to master log too, or backlog it
                    loc = dictTest['Summary File Location']
                    if loc!='NA':
                        self.WriteTestSummaryEntry(loc, line)
                outputfile.close()
            except:
                return False
        return True

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        app = QApplication(sys.argv)
        window = MyApp()
        window.show()
        try:
            sys.exit(app.exec_())
        except:
            pass
    else:
        app = CommandLineHandler()
        exitcode = app.processCommandLine(sys.argv)
        sys.exit(exitcode)
