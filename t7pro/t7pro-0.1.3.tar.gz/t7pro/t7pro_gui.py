# -*- coding: utf-8 -*-

"""package t7pro
author    Benoit Dubois
copyright FEMTO Engineering, 2019
license   GPL v3.0+
brief     GUI to handle the T7Pro DAQ board via the ethernet interface.
"""

import os
import shutil
import logging
import threading
from datetime import datetime
from time import strftime
import numpy as np
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QObject, QSettings, QDir, \
     QFileInfo
from PyQt5.QtWidgets import QMessageBox, QDialog, QFileDialog
import benutils.misc.mjdutils as mjd
from benutils.misc.datacontainer import TimeSerieContainer
from benutils.widget.real_time_plot import CurveParam
import labjack.t7.t7eth as t7dev
import labjack.t7.t7 as t7
import labjack.constants as t7cst

import t7pro.t7pro_form as form
from t7pro.constants import ORGANIZATION, APP_NAME, APP_BRIEF, AUTHOR_NAME, \
     AUTHOR_MAIL, COPYRIGHT, LICENSE
from t7pro.version import __version__


APP_CFG_DIR = QFileInfo(
    QSettings(ORGANIZATION, APP_NAME).fileName()).absolutePath()


# =============================================================================
class PreferenceDialog(form.PreferenceDialog):
    """Overide PreferenceDialog class.
    """

    def _check_interface(self):
        """Returns True if connection with device is OK.
        :returns: status of interface with device (boolean)
        """
        dev = t7dev.T7Eth(self.ip)
        if dev.connect() is True:
            try:
                _id = str(dev.get_id())
            except Exception:
                _id = ''  # Avoid error with find() when '_id' is not defined
            if _id.find(t7cst.T7_ID) >= 0:
                self._check_interface_btn.setStyleSheet(
                    "QPushButton {background-color : green; color : yellow;}")
                self._check_interface_btn.setText("OK")
            dev.close()
            return True
        self._check_interface_btn.setStyleSheet(
            "QPushButton {background-color : red; color : blue;}")
        self._check_interface_btn.setText("Error")
        return False


# =============================================================================
class ThreadedAcq(QObject):
    """ThreadedAcq class, used to provide continous data acquisition with
    blocking-read data acquisition device object. The data are sampled at
    'tsamp'. Note that sampling time must large in front of acquisition time
    and or "time constant" to ensure a correct sampling time stability.
    """

    started = pyqtSignal()  # acquisition started
    done = pyqtSignal()     # acquisition finished
    new_data = pyqtSignal(object)

    def __init__(self, dev, func=None, tsamp=1.0, parent=None):
        """Constructor
        :param dev: a data acquisition device object instance (object)
        :param func: a method of 'dev' class which return data (object)
        :param tsamp: sampling period (float)
        :returns: None
        """
        super().__init__(parent=parent)
        self._dev = dev
        self._func = func
        self._tsamp = tsamp
        self._data = None
        self._stopped = threading.Event()

    @property
    def data(self):
        """Getter of data.
        :returns: current acquired data (object)
        """
        return self._data

    @property
    def func(self):
        """Getter of func.
        :returns: a method of 'dev' class which return data (object)
        """
        return self._func

    @func.setter
    def func(self, func):
        """Setter of func.
        :param func: a method of 'dev' class which return data (object)
        :returns: None
        """
        self._func = func

    @property
    def tsamp(self):
        """Getter of tsamp.
        :returns: sampling period (float)
        """
        return self._tsamp

    @tsamp.setter
    def tsamp(self, tsamp):
        """Setter of tsamp.
        :param tsamp: sampling period (float)
        :returns: None
        """
        self._tsamp = tsamp

    @pyqtSlot()
    def stop(self):
        """Stop continuous acquisition.
        :returns: None
        """
        self._stopped.set()

    @pyqtSlot(list)
    def start(self, *args):
        """Start continuous acquisition.
        :returns: None
        """
        self._stopped.clear()
        try:
            acq_thread = threading.Thread(target=self._get_data, args=(args))
            acq_thread.start()
        except Exception as ex:
            logging.warning("Acquisition problem: %r", ex)
        self.started.emit()

    def _get_data(self, *args):
        """Virtual acquisition data method: call method '_func' of '_dev'
        instance specified with '*args' arguments. Emit signal when new data
        acquired and when acquisition is done.
        :returns: None
        """
        if self._func is None:
            logging.warning("No acquisition method specified for instance %r",
                            self._dev)
            return
        while not self._stopped.wait(self._tsamp):
            try:
                data = self._func(self._dev, *args)
            except Exception:
                logging.error("Get data error.")
            else:
                if data is not None:
                    self._data = data
                    self.new_data.emit(data)
        self.done.emit()


# =============================================================================
class T7ProGui(QObject):

    def __init__(self):
        super().__init__()
        self.data_container = TimeSerieContainer()
        self.dev = t7dev.T7Eth()
        self.producer = ThreadedAcq(self.dev,
                                    t7dev.T7Eth.get_ains_voltage,
                                    t7cst.T7_ETH_TIMEOUT)
        self.ui = form.T7ProMainWindow()
        self.actions_handling()
        self.logic_handling()

    def actions_handling(self):
        """Triggers ui actions: connects actions of ui with real actions.
        :returns: None
        """
        self.ui.action_run.triggered.connect(self.start_acq)
        self.ui.action_stop.triggered.connect(self.stop_acq)
        self.ui.action_save.triggered.connect(self.save_as)
        self.ui.action_save_cfg.triggered.connect(self.save_cfg)
        self.ui.action_load_cfg.triggered.connect(self.load_cfg)
        self.ui.action_quit.triggered.connect(self.quit)
        self.ui.action_reset.triggered.connect(self.reset_ui)
        self.ui.action_pref.triggered.connect(self.preference)
        self.ui.action_about.triggered.connect(self.about)

    def logic_handling(self):
        """Defines behaviour of logic.
        :returns: None
        """
        self.producer.done.connect(self.ui.set_configuration_mode)
        self.producer.started.connect(self.ui.set_acquisition_mode)
        self.producer.new_data.connect(self.update_container)
        self.data_container.new_data.connect(self.write_sample)
        self.data_container.new_data.connect(self.plot_data)
        self.data_container.updated.connect(self.container_updated)
        self.ui.plot_widget.dict.parameters_changed.connect(self.plot_data)

    def reset_ui(self):
        """Clears application: resets user interface to starting state.
        :returns: None
        """
        self.ui.reset()
        self.data_container.reset()

    def quit(self):
        """Quits application.
        :returns: None
        """
        self.producer.stop()
        self.ui.close()

    def update_container(self):
        """Adds the current sample(s) to the data container.
        :returns: None
        """
        now = mjd.datetime_to_mjd(datetime.utcnow())
        samples = self.producer.data
        samples.insert(0, now)
        self.data_container.add_samples(samples)

    def container_updated(self):
        """Action when data container is updated.
        :returns: None
        """
        if self.data_container.is_empty() is True:
            self.ui.action_save.setDisabled(False)
        else:
            self.ui.action_save.setEnabled(True)

    def start_acq(self):
        """Start acquisition process.
        :returns: None
        """
        # Prepare device
        self.dev.ip = QSettings().value("dev/ip")
        if self.dev.connect() is False:
            QMessageBox.warning(None, "Start problem",
                                "Connection to T7Pro failed")
            return
        self.set_ains_configuration()
        # Prepare container
        self.data_container.clear()
        self.set_data_container_configuration()
        # Start acquisition
        ains = [ain.id for ain in self.ui.module_widget.enabled_channels()]
        self.producer.start(ains)
        # Define new data filename
        settings = QSettings()
        work_dir = settings.value("ui/work_dir")
        acq_start_date = strftime("%Y%m%d-%H%M%S")
        filename = work_dir + "/" + APP_NAME + "." + acq_start_date + ".dat"
        settings.setValue("ui/file", filename)
        # Set UI in acquisition mode

    def stop_acq(self):
        """Stop acquisition process.
        :returns: None
        """
        self.producer.stop()
        self.dev.close()
        # We propose to save the last data acquired
        btn_val = self.save_box()
        if btn_val == QMessageBox.Yes:
            self.save_as()
        # We save the data files in the (volatile) system temp directory,
        # one never knows...;)
        settings = QSettings()
        file_ = settings.value("ui/file")
        shutil.move(file_, QDir.tempPath() + '/')

    def write_sample(self):
        """Writes new sample(s) in data file.
        :returns: None
        """
        settings = QSettings()
        file_ = settings.value("ui/file")
        # If file does not exist i.e. user begin a new acquisition,
        # we create an empty file with header.
        if os.path.isfile(file_) is False:
            header = self.make_header()
            with open(file_, 'ab', 0) as fd:
                np.savetxt(fname=fd, X=np.empty([0, 0]), header=header)
        #
        samples = [(self.data_container.get_array().T)[-1]]
        with open(file_, 'ab') as fd:
            np.savetxt(fname=fd, X=samples, delimiter='\t')

    def save_as(self):
        """Save data method. Call a file dialog box to choose a filename
        for the data file.
        :returns: True if file realy saved else False (bool)
        """
        settings = QSettings()
        file_ = settings.value("ui/file")
        new_file, _filter = QFileDialog(). \
            getSaveFileName(parent=None,
                            caption="Save data",
                            directory=file_,
                            filter="Data files (*.dat);;Any files (*)")
        if new_file != "":
            header = self.make_header()
            data = self.data_container.get_array().T
            with open(new_file, 'ab') as fd:
                np.savetxt(fname=fd, X=data, delimiter='\t', header=header)
                return True
        return False

    def plot_data(self):
        """Plots data on graph.
        :returns: None
        """
        for key, item in self.ui.plot_widget.dict.items():
            if item.checkState() == Qt.Checked:
                scale = item.parameters.scale
                offset = item.parameters.offset
                datax = self.data_container.data("time")
                datay = self.data_container.data(key) * scale + offset
                data = np.transpose(np.array([datax, datay]))
                try:
                    self.ui.plot_widget.curve(key).setData(data)
                except ZeroDivisionError:
                    logging.debug("Divide by zero")
                except ValueError as ex:
                    logging.warning("Exception: %r", ex)
                except Exception as ex:
                    logging.warning("Exception: %r", ex)

    def set_data_container_configuration(self):
        """Configure data container ie create adequate item from UI.
        :returns: None
        """
        ains = [ain for ain in self.ui.module_widget.enabled_channels()]
        for ain in ains:
            self.data_container.add_item(ain.id)

    def set_ains_configuration(self):
        """Set configuration of device from UI.
        :returns: None
        """
        ains = self.ui.module_widget.enabled_channels()
        ains_id = [ain.id for ain in ains]
        ains_range = [float(t7.VOLT_RANGE[ain.range].mnemo)
                      for ain in ains]
        ains_resolution = [int(t7.RESO_T7PRO[ain.resolution].mnemo)
                           for ain in ains]
        ains_settling = [float(t7.SETTLING[ain.settling].mnemo)
                         for ain in ains]
        self.dev.set_ains_range(ains_id, ains_range)
        self.dev.set_ains_resolution(ains_id, ains_resolution)
        self.dev.set_ains_settling(ains_id, ains_settling)

    def save_cfg(self):
        """Saves current device configuration. Call a file dialog box to give
        a filename for the config file.
        :returns: True if config is saved else False (bool)
        """
        settings = QSettings()
        work_dir = settings.value("ui/work_dir")
        cfg_file, _filter = QFileDialog(). \
            getSaveFileName(None,
                            "Save configuration",
                            work_dir,
                            ";;Config files (*.cfg);;Any files (*)")
        if cfg_file == "":
            return False  # Aborts if no file given
        cfg = QSettings(cfg_file, QSettings.IniFormat)
        cfg.clear()
        for channel in self.ui.module_widget.values():
            if channel.checkState() == Qt.Checked:
                parameters = self.ui.plot_widget.legend(channel.id).parameters
                ch_nb = str(channel.id)
                label = parameters.label
                _range = str(channel.range)
                resolution = str(channel.resolution)
                settling = str(channel.settling)
                scale = str(parameters.scale)
                offset = str(parameters.offset)
                cfg.beginGroup(ch_nb)
                cfg.setValue("label", label)
                cfg.setValue("range", _range)
                cfg.setValue("settling", settling)
                cfg.setValue("resolution", resolution)
                cfg.setValue("scale", scale)
                cfg.setValue("offset", offset)
                cfg.endGroup()
        return True

    def load_cfg(self):
        """Loads a device configuration. Call a file dialog box to select
        the config file.
        :returns: True if config is loaded else False (bool)
        """
        settings = QSettings()
        work_dir = settings.value("ui/work_dir")
        cfg_file, _filter = QFileDialog(). \
            getOpenFileName(None,
                            "Load configuration",
                            work_dir,
                            "Config files (*.cfg);;Any files (*)")
        if cfg_file == "":
            return False  # Aborts if no file given
        cfg = QSettings(cfg_file, QSettings.IniFormat)
        for channel in self.ui.module_widget.values():
            ch_nb = str(channel.id)
            if ch_nb in cfg.childGroups():
                cfg.beginGroup(ch_nb)
                label = cfg.value("label")
                _range = int(cfg.value("range"))
                resolution = int(cfg.value("resolution"))
                settling = int(cfg.value("settling"))
                scale = float(cfg.value("scale"))
                offset = float(cfg.value("offset"))
                cfg.endGroup()
                channel.setState(Qt.Checked)
                channel.set_range(_range)
                channel.set_resolution(resolution)
                channel.set_settling(settling)
                self.ui.plot_widget.legend(channel.id).set_parameters(
                    CurveParam(label, scale, offset))
            else:
                channel.reset()
        return True

    def make_header(self):
        """Collects data information (channel, measurement type and parameters)
        to be used as header for a data file.
        :returns: the data header (str)
        """
        header = ""
        for channel in self.ui.module_widget.enabled_channels():
            ch_nb = str(channel.id)
            func = str(channel.param_wdgt.func_cbox.currentText())
            rang = str(channel.param_wdgt.range_cbox.currentText())
            reso = str(channel.param_wdgt.reso_cbox.currentText())
            header += "Channel(" + ch_nb + "), " \
            + self.ui.plot_widget.legend(channel.id).parameters.label \
            + "; " + func + "; " + rang + "; " + reso + "; " + "; scale:" \
            + str(self.ui.plot_widget.legend(channel.id).parameters.scale) \
            + "; offset:" \
            + str(self.ui.plot_widget.legend(channel.id).parameters.offset) \
            + "\n"
        return header

    def preference(self):
        """Displays the preference message box.
        :returns: None
        """
        settings = QSettings()
        dialog = PreferenceDialog(settings.value("dev/ip"),
                                  settings.value("ui/work_dir"))
        dialog.setParent(None, Qt.Dialog)
        retval = dialog.exec_()
        if retval == QDialog.Accepted:
            settings.setValue("dev/ip", dialog.ip)
            settings.setValue("ui/work_dir", dialog.workspace_directory)

    @staticmethod
    def save_box():
        """Display a message box requesting confirmation to save the data file.
        Returns the value of the button clicked.
        :returns: the value of the button clicked (int)
        """
        msg_box = QMessageBox()
        msg_box.setWindowTitle(APP_NAME)
        msg_box.setText("Acquisition stopped")
        msg_box.setInformativeText("Save data?")
        msg_box.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msg_box.setDefaultButton(QMessageBox.Yes)
        btn_val = msg_box.exec_()
        return btn_val

    @staticmethod
    def about():
        """Displays an about message box.
        :returns: None
        """
        QMessageBox.about(None, "About " + APP_NAME,
                          "<b>" + APP_NAME +  " " + __version__ + "</b><br>" +
                          APP_BRIEF + ".<br>" +
                          "Author " + AUTHOR_NAME +
                          ", " + AUTHOR_MAIL + " .<br>" +
                          "Copyright " + COPYRIGHT + ".<br>" +
                          "Licensed under the " + LICENSE)

    @staticmethod
    def pt100_voltage_to_temperature(i0, v):
        """Return the temperature relative to (I,V) characteristic of a pt100
        sensor. Note that the response of a pt100 is nonlinear,
        but the expression works well from about -40 to +150 degree Celsius.
        :param i0: current through sensor (float)
        :param v: voltage accross sensor (float)
        :returns: the temperature value (float)
        """
        return (2.604 * v / i0) - 260.4
