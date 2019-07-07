#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import appdirs
import json
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QMainWindow
from PyQt5.QtWidgets import QMenuBar, QMenu, QFileDialog, QLabel, QMessageBox
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QSizePolicy, QGridLayout

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # to import from this project without instalation
from client.config import ClientConfig
from videowidget import VideoWidget
import base_plugin

DEFAULT_SETTING_FILE_NAME = "settings.json"
APP_NAME = "automatic-behavior-analysis-client"

class Client_GUI(QMainWindow):
    onOpenFile = pyqtSignal(str)

    def __init__(self, title, min_width, min_height, config):
        super().__init__()

        self._settings = self._read_settings() # TODO: send to fcn filename from config

        self.config = config
        if config.input_file:
            self._load_on_connect = config.input_file
        self._skip_frames = config.skip_frames
        self._sample_delta = self._settings.get('sample_delta', 10)
        config.limit_boxes = self._settings.get('limit_boxes', False)
        config.detect_motion = self._settings.get('detect_motion', True)
        config.inner_detection = self._settings.get('inner_detection', False)

        self._title = title #  type:String
        self._min_width = min_width
        self._min_height = min_height

        self.initUI()


    def initUI(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.setWindowTitle(self._title)

        ### Создание и конфигурация меню ###
        self._menu_bar = self.menuBar()

        self._menu_file = self._menu_bar.addMenu("File")
        action = self._menu_file.addAction("Open file")
        action.triggered.connect(self.open_file_clicked)
        self._menu_file.addSeparator()
        action = self._menu_file.addAction("Exit")
        action.triggered.connect(self.exit_clicked)

        ### Создание и получение строки состояния ###

        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Ready')

        # Load plugin and components from it
        self._plugin = self.load_plugin()
        self.mediasrc = self._plugin.get_media_source_processor()
        self._rtStatisticWidget = self._plugin.get_rt_statistic_widget()
        self._summaryStatisticWidget = self._plugin.get_summary_statistic_widget()

        ws = self._settings.get('window') or {}
        q = QDesktopWidget().availableGeometry() # Get screen size

        ### Основные виджеты ###
        self._main_widget = QWidget()
        self._main_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Основной виджет с видеоплеером
        self._videoview = VideoWidget(media_source=self.mediasrc, parent=self)
        self._videoview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._gridLayout = QGridLayout()
        self._gridLayout.setSpacing(5)
        self._gridLayout.addWidget(self._videoview, 0, 0, -1, 10)
        self._gridLayout.addWidget(QLabel("Realtime statistic"), 0, 10, 1, 1)
        self._gridLayout.addWidget(self._rtStatisticWidget, 1, 10, 10, 3)
        self._gridLayout.addWidget(QLabel("Summary statistic"), 11, 10, 1, 1)
        self._gridLayout.addWidget(self._summaryStatisticWidget, 12, 10, 10, 3)

        self._main_widget.setLayout(self._gridLayout)
        self.setCentralWidget(self._main_widget)

        # Set main windows geometry
        width = ws.get('width') or max(q.width() // 2, self._min_width)
        height = ws.get('height') or max(q.height() // 2, self._min_height)
        x = ws.get('x') or (q.width() - width) // 2
        y = ws.get('y') or (q.height() - height) // 2
        self.setGeometry(x, y, width, height)

        # Show gui
        self.show()

    def load_plugin(self):
        plugin = None
        if self.config.media_source_type == 'simpleCam':
            plugin = base_plugin.SimplePlugin(self.config)
        elif self.config.media_source_type == 'nnCam':
            plugin = base_plugin.SimpleNNPreprocessPlugin(self.config)
        elif self.config.media_source_type == 'nnVideo':
            import dog_plugin
            plugin = dog_plugin.SleepDogPlugin(self.config)
            plugin.set_status_bar(self.status_bar)
            plugin.set_menu(self._menu_bar)

        self.onOpenFile.connect(plugin.onOpenFile)
        return plugin

    def _read_settings(self, filename=None):
        """
            Read settings from file or default location
            @args:
        """
        filename = filename or os.path.join(appdirs.user_config_dir(APP_NAME, False), DEFAULT_SETTING_FILE_NAME)
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                settings = json.load(file)
                # from pprint import pprint
                # print("Loaded settings:")
                # pprint(settings, indent=2)
                return settings
        except:
            return {}

    @pyqtSlot()
    def open_file_clicked(self):
        """
        Обработчик нажатия на открыть файл
        """
        fileName = QFileDialog.getOpenFileName(self, "Open Video",
                self._settings.get('last_open_dir', "./"),
                "Video files (*.mp4) ;; All files (*.*)")[0]
        if len(fileName) > 0:
            self._settings['last_open_dir'] = os.path.dirname(fileName)
            print("Opening file: {}".format(fileName))
            self.open_file(fileName)

    @pyqtSlot()
    def exit_clicked(self):
        QCoreApplication.instance().quit()

    def open_file(self, filename):
        self.onOpenFile.emit(filename)

    def closeEvent(self, event):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle('Exit')
        msg.setText('Did you save the statistics? (to save the statistics, give the dogs names and click on the "Save statistic" button)')   
        no = msg.addButton(
            'No', QMessageBox.NoRole)
        yes = msg.addButton(
            'Yes', QMessageBox.YesRole)
        msg.setDefaultButton(yes)
        msg.exec_()
        msg.deleteLater()
        if msg.clickedButton() is yes:
            event.accept()
        else:
            event.ignore()

def main():
    """Application entry point"""
    config = ClientConfig(os.path.join(os.path.dirname(__file__), "config.json"))
    parser = argparse.ArgumentParser(description="Data analysis client")
    parser.add_argument('--ip', help="Server IP address or hostname", default=argparse.SUPPRESS)
    parser.add_argument('--port', help="Server port", type=int, default=argparse.SUPPRESS)
    parser.add_argument('--protocol', default=config.protocol, help="Server protocol", choices=['tcp', 'websocket'])
    parser.add_argument('--skip-frames', help="Skip (don't process) every k frames", default=0, type=int)
    parser.add_argument('--verbose', help="Show detailed debug messages", action='store_true')
    parser.add_argument('--media_source_type',
                        default=config.media_source_type,
                        help="Type of mediasource. Can be: simpleCam, nnCam",
                        choices=['simpleCam', 'nnCam', 'nnVideo'])
    parser.add_argument('input_file', nargs='?', help="Input file")
    args = vars(parser.parse_args())
    config.update(args)
    config.auto_connect = 'ip' in args or 'port' in args or 'input' in args

    if config.auto_connect:
        print("Starting client for {}:{}".format(config.ip, config.port))
    else:
        print("Warning: Have not server config")

    app = QApplication(sys.argv)
    gui = Client_GUI("Automatic Behavior Analysis", 320, 240, config)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()