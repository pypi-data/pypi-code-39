# -*- coding: utf-8 -*-

"""package t7pro
author    Benoit Dubois
copyright FEMTO Engineering, 2019
license   GPL v3.0+
brief     UI to handle the T7Pro DAQ board.
"""

from PyQt5 import Qt
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSignalMapper
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, \
    QAction, QComboBox, QVBoxLayout, QCheckBox, QTabWidget, QDialog, \
    QGroupBox, QLineEdit, QDialogButtonBox, QScrollArea, \
    QPushButton, QToolButton, QFileDialog
from benutils.widget.real_time_plot import EPlotWidget
from benutils.widget.flowlayout import FlowLayout
import labjack.t7.t7 as t7

from t7pro.constants import APP_NAME


# =============================================================================
class PreferenceDialog(QDialog):
    """PreferenceDialog class, generates the ui of the preference form.
    """

    workspace_changed = pyqtSignal(str)

    def __init__(self, ip="", workspace_dir="", parent=None):
        """Constructor.
        :param dev: device class instance (object)
        :param ip: IP of T7Pro device (str)
        :param workspace_dir: workspace where data files are writed (str)
        :param parent: parent object (object)
        :returns: None
        """
        super().__init__(parent=parent)
        self.setWindowTitle("Preferences")
        # Lays out
        dev_gbox = QGroupBox("Interface")
        self.ip_led = QLineEdit(ip)
        self.ip_led.setInputMask("000.000.000.000;")
        self._check_interface_btn = QPushButton("Check")
        self._check_interface_btn.setToolTip("Check connection with device")
        self.workspace_btn = QToolButton()
        self.workspace_btn.setToolButtonStyle(Qt.Qt.ToolButtonIconOnly)
        self.workspace_lbl = QLabel(workspace_dir)
        dev_lay = QVBoxLayout()
        dev_lay.addWidget(QLabel("IP"))
        dev_lay.addWidget(self.ip_led)
        dev_lay.addWidget(self._check_interface_btn)
        dev_lay.addWidget(QLabel("Workspace directory"))
        dev_lay.addWidget(self.workspace_btn)
        dev_lay.addWidget(self.workspace_lbl)
        dev_gbox.setLayout(dev_lay)
        self._btn_box = QDialogButtonBox(QDialogButtonBox.Ok |
                                         QDialogButtonBox.Cancel)
        main_lay = QVBoxLayout()
        main_lay.addWidget(dev_gbox)
        main_lay.addWidget(self._btn_box)
        self.setLayout(main_lay)
        # Basic logic
        self._btn_box.accepted.connect(self.accept)
        self._btn_box.rejected.connect(self.close)
        self._check_interface_btn.released.connect(self._check_interface)
        # Specific workspace logic
        self.workspace_changed.connect(self.workspace_lbl.setText)
        self.action_workspace = QAction(QIcon.fromTheme("folder-new"),
                                        "Choose &workspace", self)
        self.action_workspace.setStatusTip("Choose workspace directory")
        self.workspace_btn.setDefaultAction(self.action_workspace)
        self.action_workspace.triggered.connect(self._workspace_dialog)

    def _check_interface(self):
        """To be subclassed.
        """
        pass

    @pyqtSlot()
    def _workspace_dialog(self):
        """Choose path to workspace. Call a file dialog box to choose
        the working workspace.
        :returns: choosen workspace else an empty string (str)
        """
        workspace_dir = QFileDialog(). \
            getExistingDirectory(parent=None,
                                 caption="Choose workspace directory",
                                 directory=self.workspace_lbl.text())
        if workspace_dir == "":
            return ""
        self.workspace_changed.emit(workspace_dir)
        return workspace_dir

    @property
    def ip(self):
        """Getter of the IP value.
        :returns: IP of device (str)
        """
        return self.ip_led.text()

    @property
    def workspace_directory(self):
        """Getter of the data workspace value.
        :returns: workspace where data files are writed (str)
        """
        return self.workspace_lbl.text()


# =============================================================================
class ParamWdgt(QWidget):
    """ParamWdgt class, used to handle the graphical configuration of a
    channel of the T7Pro module.
    """

    function_changed = pyqtSignal(int)
    range_changed = pyqtSignal(int)
    resolution_changed = pyqtSignal(int)
    settling_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        """Constructor: setup ui.
        :retuns: None
        """
        super().__init__(parent=parent)
        self.func_cbox = QComboBox()
        self.range_cbox = QComboBox()
        self.reso_cbox = QComboBox()
        self.settling_cbox = QComboBox()
        # Lays out
        layout = QVBoxLayout()
        layout.addWidget(self.func_cbox)
        layout.addWidget(self.range_cbox)
        layout.addWidget(self.reso_cbox)
        layout.addWidget(self.settling_cbox)
        self.setLayout(layout)
        # Generates signals
        self.func_cbox.currentIndexChanged.connect(self.function_changed.emit)
        self.reso_cbox.currentIndexChanged.connect(
            self.resolution_changed.emit)
        self.range_cbox.currentIndexChanged.connect(self.range_changed.emit)
        self.settling_cbox.currentIndexChanged.connect(
            self.settling_changed.emit)
        # UI handling
        self._ui_handling()
        # Inits widgets
        for func in t7.FUNCTION:
            self.func_cbox.addItem(func.caption)
        for reso in t7.RESO_T7PRO:
            self.reso_cbox.addItem(reso.caption)
        for _range in t7.VOLT_RANGE:
            self.range_cbox.addItem(_range.caption)
        for settling in t7.SETTLING:
            self.settling_cbox.addItem(settling.caption)

    def _ui_handling(self):
        """Basic ui handling. Handles widget enabling/disabling.
        Resolution and integration time value are linked.
        :returns: None
        """
        # todo: self.func_cbox.currentIndexChanged.connect(self.set_range_list)
        pass

    def reset(self):
        """Resets the widget.
        :returns: None
        """
        self.func_cbox.setCurrentIndex(0)
        self.range_cbox.setCurrentIndex(0)
        self.reso_cbox.setCurrentIndex(0)
        self.settling_cbox.setCurrentIndex(0)

    @property
    def function(self):
        """Getter for function property.
        :returns: index representing the selected function (int)
        """
        return self.func_cbox.currentIndex()

    @property
    def range(self):
        """Getter for range property.
        :returns: index representing the selected range (int)
        """
        return self.range_cbox.currentIndex()

    @property
    def resolution(self):
        """Getter for resolution property.
        :returns: index representing the selected resolution (int)
        """
        return self.reso_cbox.currentIndex()

    @property
    def settling(self):
        """Getter for integration time property.
        :returns: index representing the selected integration time (int)
        """
        return self.settling_cbox.currentIndex()

    def set_function(self, value):
        """Setter for function property.
        :param value: index representing the selected function (int)
        :returns: None
        """
        self.func_cbox.setCurrentIndex(value)

    def set_range(self, value):
        """Setter for range property.
        :param value: index representing the selected range (int)
        :returns: None
        """
        self.range_cbox.setCurrentIndex(value)

    def set_resolution(self, value):
        """Setter for resolution property.
        :param value: index representing the selected resolution (int)
        :returns: None
        """
        self.reso_cbox.setCurrentIndex(value)

    def set_settling(self, value):
        """Setter for integration time property.
        :param value: index representing the selected integration time (int)
        :returns: None
        """
        self.settling_cbox.setCurrentIndex(value)

    """@pyqtSlot(int)
    def set_range_list(self, func_id):
        Sets a new item list in the range combobox in respect with function
        sets in function combobox widget.
        :param func_id: current function identifier (int)
        :returns: None

        self.range_cbox.clear()
        range_list = t7.FUNCTION[func_id].list
        for item in range_list:
            self.range_cbox.addItem(item.caption))"""


# =============================================================================
class ChannelWdgt(QWidget):
    """ChannelWdgt class, used to handle the graphical configuration of a
    channel of the T7Pro board.
    """

    state_changed = pyqtSignal(int)
    function_changed = pyqtSignal(int)
    range_changed = pyqtSignal(int)
    resolution_changed = pyqtSignal(int)
    settling_changed = pyqtSignal(int)

    def __init__(self, id_num, parent=None):
        """Constructor: setup ui.
        :parma id_num: unique identification number (int)
        :retuns: None
        """
        super().__init__(parent=parent)
        self.id = id_num
        self.en_ckbox = QCheckBox("Enabled")
        self.label = QLabel("Channel " + str(id_num))
        self.param_wdgt = ParamWdgt()
        # Lays out
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.en_ckbox)
        layout.addWidget(self.param_wdgt)
        self.setLayout(layout)
        # Generates signals
        self.param_wdgt.function_changed.connect(self.function_changed.emit)
        self.param_wdgt.range_changed.connect(self.range_changed.emit)
        self.param_wdgt.resolution_changed.connect(
            self.resolution_changed.emit)
        self.param_wdgt.settling_changed.connect(self.settling_changed.emit)
        self.en_ckbox.stateChanged.connect(self.state_changed.emit)
        # UI handling
        self._ui_handling()
        # Inits widget
        self.reset()

    def _ui_handling(self):
        """Basic ui handling. Handles widget enabling/disabling.
        :returns: None
        """
        self.en_ckbox.stateChanged.connect(self.handle_state_change)

    def reset(self):
        """Resets the widget.
        :returns: None
        """
        self.param_wdgt.reset()
        self.setState(Qt.Qt.Unchecked)
        self.setEnabled(False)

    @property
    def function(self):
        """Getter for function property.
        :returns: index representing the selected function (int)
        """
        return self.param_wdgt.function

    @property
    def range(self):
        """Getter for range property.
        :returns: index representing the selected range (int)
        """
        return self.param_wdgt.range

    @property
    def resolution(self):
        """Getter for resolution property.
        :returns: index representing the selected resolution (int)
        """
        return self.param_wdgt.resolution

    @property
    def settling(self):
        """Getter for integration time property.
        :returns: index representing the selected integration time (int)
        """
        return self.param_wdgt.settling

    def set_function(self, value):
        """Setter for function property.
        :param value: index representing the selected function (int)
        :returns: None
        """
        self.param_wdgt.set_function(value)

    def set_range(self, value):
        """Setter for range property.
        :param value: index representing the selected range (int)
        :returns: None
        """
        self.param_wdgt.set_range(value)

    def set_resolution(self, value):
        """Setter for resolution property.
        :param value: index representing the selected resolution (int)
        :returns: None
        """
        self.param_wdgt.set_resolution(value)

    def set_settling(self, value):
        """Setter for integration time property.
        :param value: index representing the selected integration time (int)
        :returns: None
        """
        self.param_wdgt.set_settling(value)

    def checkState(self):
        """Redefines method: returns the state of widget ie the state of the
        en_ckbox widget instead of the state of the widget itself, because
        the en_ckbox widget master the state of the widget.
        :returns: the state of the check box (int)
        """
        return self.en_ckbox.checkState()

    def setState(self, state):
        """Sets state property. See checkState().
        :param state: the state of the check box (int)
        """
        self.en_ckbox.setCheckState(state)

    def isEnabled(self):
        """Redefines method: returns the state of widget ie the state of the
        en_ckbox widget instead of the state of the widget itself, because
        the en_ckbox widget master the state of the widget.
        :returns: State of widget (bool)
        """
        return self.en_ckbox.isEnabled()

    def setEnabled(self, flag=True):
        """Redefines method: enables/disables whole widgets except en_ckbox
        widget, because the en_ckbox called this function.
        :param flag: new flag (bool)
        :returns: None
        """
        self.param_wdgt.setEnabled(flag)

    def handle_state_change(self, state):
        """Handles widget in respect with QCheckBox state.
        :param state: new state (int)
        :returns: None
        """
        self.setEnabled(True if state == Qt.Qt.Checked else False)


# =============================================================================
class T7ProChannelsWidget(QWidget):
    """T7ProChannelsWidget class, used to handle the graphical configuration of
    the T7Pro board.
    """

    channel_state_changed = pyqtSignal(int)
    channel_function_changed = pyqtSignal(int)
    channel_range_changed = pyqtSignal(int)
    channel_resolution_changed = pyqtSignal(int)
    channel_settling_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        """Constructor.
        :returns: None
        """
        super().__init__(parent=parent)
        self._channels = {}
        for id_key in range(14):
            self._channels[id_key] = ChannelWdgt(id_key)
        # Layout
        scroll_layout = QVBoxLayout(self)
        scroll = QScrollArea()
        scroll_layout.addWidget(scroll)
        scroll_wdgt = QWidget(self)
        dyn_layout = FlowLayout(scroll_wdgt)
        for channel in self._channels.values():
            dyn_layout.addWidget(channel)
        scroll.setWidget(scroll_wdgt)
        scroll.setWidgetResizable(True)
        # Signals handling
        # # channel_state_changed()
        state_signal_mapper = QSignalMapper(self)
        for key, channel in self._channels.items():
            state_signal_mapper.setMapping(channel, key)
            channel.state_changed.connect(state_signal_mapper.map)
        state_signal_mapper.mapped.connect(self.channel_state_changed)
        # # channel_function_changed()
        function_signal_mapper = QSignalMapper(self)
        for key, channel in self._channels.items():
            function_signal_mapper.setMapping(channel, key)
            channel.function_changed.connect(function_signal_mapper.map)
        function_signal_mapper.mapped.connect(self.channel_function_changed)
        # # channel_range_changed()
        range_signal_mapper = QSignalMapper(self)
        for key, channel in self._channels.items():
            range_signal_mapper.setMapping(channel, key)
            channel.range_changed.connect(range_signal_mapper.map)
        range_signal_mapper.mapped.connect(self.channel_range_changed)
        # # channel_resolution_changed()
        resolution_signal_mapper = QSignalMapper(self)
        for key, channel in self._channels.items():
            resolution_signal_mapper.setMapping(channel, key)
            channel.resolution_changed.connect(resolution_signal_mapper.map)
        resolution_signal_mapper.mapped.connect(
            self.channel_resolution_changed)
        # # channel_settling_changed()
        settling_signal_mapper = QSignalMapper(self)
        for key, channel in self._channels.items():
            settling_signal_mapper.setMapping(channel, key)
            channel.settling_changed.connect(settling_signal_mapper.map)
        settling_signal_mapper.mapped.connect(self.channel_settling_changed)

    def __iter__(self):
        """Iterator: iterates over channels dict.
        """
        return iter(self._channels)

    def values(self):
        """Iterator: iterates over channels dict.
        """
        return iter(self._channels.values())

    def enabled_channels(self):
        """Getter of the list of enabled channel object (list).
        :returns: the list of enabled channel object (list)
        """
        enable_channel_list = []
        for channel in self._channels.values():
            if channel.en_ckbox.checkState() == Qt.Qt.Checked:
                enable_channel_list.append(channel)
        return enable_channel_list

    def reset(self):
        """Resets UI.
        :returns: None
        """
        for channel in self._channels.values():
            channel.reset()

    @property
    def channels(self):
        """Getter of the dictionnary of channel object (dict).
        :returns: the dictionnary of channel object (dict)
        """
        return self._channels

    def channel(self, id_key):
        """Getter of channel widget object (ChannelWdgt).
        :param id_key: key index of channel in the dict channel (str)
        :returns: a channel widget object (ChannelWdgt)
        """
        return self._channels[id_key]


# =============================================================================
class T7ProWidget(QWidget):
    """T7ProWidget class, main interface of the UI of the data log form.
    """

    CHANNEL_KEYS_LIST = range(14)

    def __init__(self, parent=None):
        """Constructor.
        :returns: None
        """
        super().__init__(parent=parent)
        # Lays out
        tab = QTabWidget()
        self.module_widget = T7ProChannelsWidget()
        self.plot_widget = self._build_plot_widget(self.CHANNEL_KEYS_LIST)
        tab.addTab(self.module_widget, "Configuration")
        tab.addTab(self.plot_widget, "Plot data")
        # tab.addTab(self.dev_widget, "Analyze")
        layout = QVBoxLayout()
        layout.addWidget(tab)
        self.setLayout(layout)
        # Initialization
        for legend in self.plot_widget.dict.legends.values():
            legend.setDisabled(True)
        # Local ui handling
        self.module_widget.channel_state_changed.connect(
            self._channel_state_change)
        self.plot_widget.dict.state_changed.connect(self._update_plot_list)

    @staticmethod
    def _build_plot_widget(channel_keys):
        """Builds widget dedicated to data plotting.
        :param channel_keys: list of key for each of channel in widget (list)
        :returns: data plotting widget (EPlotWidget)
        """
        plot_widget = EPlotWidget(channel_keys)
        plot_widget.plot.setTitle("Monitoring")
        return plot_widget

    @staticmethod
    def _build_dev_widget():
        """Builds layout dedicated to deviation analyze.
        :returns: deviation plotting widget (AdevPlotWidget)
        """
        # dev_widget = DevPlotWidget()
        # return dev_widget
        pass

    @pyqtSlot(object, int)
    def _update_plot_list(self, scan, state):
        """Updates plot list, the list of channel to plot.
        :param scan: the scan number of the channel updated (object)
        :param state: the state of the channel updated (Qt.State) (int)
        :returns: None
        """
        if state == Qt.Qt.Checked:
            self.plot_widget.hide(scan, False)
        else:
            self.plot_widget.hide(scan, True)

    @pyqtSlot(int)
    def _channel_state_change(self, scan):
        """Updates scan list, the list of channel to scan and update legend
        state of plot widget.
        :param scan: scan number of the channel updated (int)
        :returns: None
        """
        state = self.module_widget.channel(scan).checkState()
        if state == Qt.Qt.Checked:
            self.plot_widget.add_curve(scan)
            self.plot_widget.legend(scan).setEnabled(True)
            self.plot_widget.legend(scan).setState(Qt.Qt.Checked)
        else:
            self.plot_widget.legend(scan).setDisabled(True)
            self.plot_widget.legend(scan).setState(Qt.Qt.Unchecked)
            self.plot_widget.remove_curve(scan)


# =============================================================================
class T7ProMainWindow(QMainWindow):
    """MainWindow class, main interface of the UI of the data log form.
    """

    def __init__(self, parent=None):
        """Constructor.
        :returns: None
        """
        super().__init__(parent=parent)
        self.setWindowTitle(APP_NAME)
        # Lays out
        self._create_actions()
        self._menu_bar = self.menuBar()
        self._populate_menubar()
        self._tool_bar = self.addToolBar("Tool Bar")
        self._populate_toolbar()
        self._tool_bar.setMovable(True)
        self._tool_bar.setFloatable(False)
        self._tool_bar.setAllowedAreas(Qt.Qt.AllToolBarAreas)
        self._status_bar = self.statusBar()
        self._data_log_wdgt = T7ProWidget()
        self.setCentralWidget(self._data_log_wdgt)
        # UI handling
        self._ui_handling()
        # Initialization of UI
        self.reset()

    def reset(self):
        """Resets form.
        :returns: None
        """
        self._data_log_wdgt.module_widget.reset()
        self._data_log_wdgt.plot_widget.reset()
        self.action_run.setEnabled(False)
        self.action_stop.setEnabled(False)
        self.action_save.setEnabled(False)
        self.action_reset.setEnabled(False)

    def set_configuration_mode(self):
        """Set UI in configuration (normal) mode, i.e. all configuration
        widgets must be usable.
        returns: None
        """
        self.action_run.setEnabled(True)
        self.action_stop.setEnabled(False)
        self.action_reset.setEnabled(True)
        self.action_save.setEnabled(True)
        self._data_log_wdgt.module_widget.setEnabled(True)

    def set_acquisition_mode(self):
        """Set UI in acquisition mode, i.e. all configuration widgets
        must not be usable.
        returns: None
        """
        self.action_run.setEnabled(False)
        self.action_stop.setEnabled(True)
        self.action_reset.setEnabled(False)
        self.action_save.setEnabled(False)
        self._data_log_wdgt.module_widget.setEnabled(False)

    @property
    def module_widget(self):
        """Getter of module widget (T7ProChannelsWidget).
        :returns: a module widget (T7ProChannelsWidget)
        """
        return self._data_log_wdgt.module_widget

    @property
    def plot_widget(self):
        """Getter of plot widget (EPlotWidget).
        :returns: a plot widget (EPlotWidget)
        """
        return self._data_log_wdgt.plot_widget

    @property
    def dev_widget(self):
        """Getter of deviation widget (DevPlotWidget).
        :returns: a deviation widget (DevPlotWidget)
        """
        return self._data_log_wdgt.dev_widget

    def _ui_handling(self):
        """Basic (local) ui handling.
        :returns: None
        """
        # Handles UI when the state of a channel changes
        self._data_log_wdgt.module_widget.channel_state_changed.connect(
            self._channel_state_change)

    @pyqtSlot()
    def _channel_state_change(self):
        """Handles ui when the state of channels changes:
        updates the state of the run button of bars.
        :returns: None
        """
        if not self._data_log_wdgt.module_widget.enabled_channels():
            # If no channel selected, do not allow start of acquisition
            self.action_run.setDisabled(True)
        else:
            # If channel(s) selected, allow start of acquisition
            self.action_run.setEnabled(True)

    def _create_actions(self):
        """Creates actions used with bar widgets.
        :returns: None
        """
        self.action_save = QAction(QIcon.fromTheme("document-save"),
                                   "&Save", self)
        self.action_save.setStatusTip("Save data")
        self.action_save.setShortcut('Ctrl+S')

        self.action_save_cfg = QAction("Save &Config", self)
        self.action_save_cfg.setStatusTip("Save the configuration for later")
        self.action_save_cfg.setShortcut('Ctrl+C')

        self.action_load_cfg = QAction("&Load Config", self)
        self.action_load_cfg.setStatusTip("Load a previous configuration")
        self.action_load_cfg.setShortcut('Ctrl+L')

        self.action_quit = QAction(QIcon.fromTheme("application-exit"),
                                   "&Quit", self)
        self.action_quit.setStatusTip("Exit application")
        self.action_quit.setShortcut('Ctrl+Q')

        self.action_reset = QAction(QIcon.fromTheme("edit-clear"),
                                    "R&eset", self)
        self.action_reset.setStatusTip("Reset the configuration")
        self.action_reset.setShortcut('Ctrl+E')

        self.action_pref = QAction(QIcon.fromTheme("preferences-system"),
                                   "&Preferences", self)
        self.action_pref.setStatusTip("Open preference dialog form")
        self.action_pref.setShortcut('Ctrl+P')

        self.action_run = QAction(QIcon.fromTheme("system-run"),
                                  "&Run", self)
        self.action_run.setStatusTip("Start acquisition")
        self.action_run.setShortcut('Ctrl+R')

        self.action_stop = QAction(QIcon.fromTheme("process-stop"),
                                   "S&top", self)
        self.action_stop.setStatusTip("Stop acquisition")
        self.action_stop.setShortcut('Ctrl+T')

        self.action_about = QAction(QIcon.fromTheme("help-about"),
                                    "A&bout", self)
        self.action_about.setStatusTip("About " + APP_NAME)
        self.action_about.setShortcut('Ctrl+B')

    def _populate_menubar(self):
        """Populates the menu bar of the UI
        :returns: None
        """
        self._menu_bar.menu_file = self._menu_bar.addMenu("&File")
        self._menu_bar.menu_edit = self._menu_bar.addMenu("&Edit")
        self._menu_bar.menu_process = self._menu_bar.addMenu("&Process")
        self._menu_bar.menu_help = self._menu_bar.addMenu("&Help")
        self._menu_bar.menu_file.addAction(self.action_save)
        self._menu_bar.menu_file.addSeparator()
        self._menu_bar.menu_file.addAction(self.action_save_cfg)
        self._menu_bar.menu_file.addAction(self.action_load_cfg)
        self._menu_bar.menu_file.addSeparator()
        self._menu_bar.menu_file.addAction(self.action_quit)
        self._menu_bar.menu_edit.addAction(self.action_pref)
        self._menu_bar.menu_process.addAction(self.action_run)
        self._menu_bar.menu_process.addAction(self.action_stop)
        self._menu_bar.menu_process.addAction(self.action_reset)
        self._menu_bar.menu_help.addAction(self.action_about)

    def _populate_toolbar(self):
        """Populates the tool bar of the UI
        :returns: None
        """
        self._tool_bar.addAction(self.action_run)
        self._tool_bar.addAction(self.action_stop)
        self._tool_bar.addAction(self.action_reset)
        self._tool_bar.addAction(self.action_save)


# =============================================================================
def test_display_ui():
    """Displays the main UI.
    """
    import sys

    def print_slot(arg):
        """Print 'arg' to standard output.
        :param arg: data to display (any)
        :returns: None
        """
        print("ui.print_slot.arg", arg)

    app = QApplication(sys.argv)
    # ui = ChannelWdgt(101, ("DC Voltage", "AC Voltage", "Resistance"))
    # ui = T7ProChannelsWidget(1)
    # ui = T7ProWidget()
    ui = T7ProMainWindow()
    ui.module_widget.channel_state_changed.connect(print_slot)
    ui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    test_display_ui()
