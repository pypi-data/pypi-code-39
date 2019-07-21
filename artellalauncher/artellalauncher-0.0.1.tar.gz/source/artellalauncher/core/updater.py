#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains implementation to create Artella launchers
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import os
import json
import tempfile
import traceback

from tpQtLib.Qt.QtCore import *
from tpQtLib.Qt.QtWidgets import *

from tpPyUtils import path as path_utils

from tpQtLib.core import base
from tpQtLib.core import qtutils

import artellapipe
import artellalauncher
from artellalauncher.core import defines
from artellalauncher.utils import download


class ArtellaUpdater(base.BaseWidget, object):

    UPDATER_CONFIG_PATH = artellalauncher.get_updater_config_path()

    def __init__(self, launcher, parent=None):

        self._launcher = launcher
        self._version = None
        self._tools_filename = None
        self._tools_env_var = None
        self._repository_url = None
        self._last_version_file_name = None
        self._progress_colors = list()

        self.init_config()

        super(ArtellaUpdater, self).__init__(parent=parent)

    def get_main_layout(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(5, 2, 5, 2)
        main_layout.setSpacing(2)
        return main_layout

    def ui(self):
        super(ArtellaUpdater, self).ui()

        self.setWindowFlags(Qt.FramelessWindowHint)

        self._progress_bar = QProgressBar()
        self.main_layout.addWidget(self._progress_bar)
        self._progress_bar.setMaximum(100)
        self._progress_bar.setTextVisible(False)
        self._progress_bar.setStyleSheet("QProgressBar {border: 0px solid grey; border-radius:4px; padding:0px} QProgressBar::chunk {background: qlineargradient(x1: 0, y1: 1, x2: 1, y2: 1, stop: 0 rgb(" + str(self.progress_colors[0]) + "), stop: 1 rgb(" + str(self.progress_colors[1]) + ")); }")

        self._progress_text = QLabel('Downloading {} Tools ...'.format(self.launcher.name.title()))
        self._progress_text.setAlignment(Qt.AlignCenter)
        self._progress_text.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 180); color : white; }")
        font = self._progress_text.font()
        font.setPointSize(10)
        self._progress_text.setFont(font)
        self.main_layout.addWidget(self._progress_text)

    @property
    def launcher(self):
        """
        Returns launcher linked to this updater
        :return: ArtellaLauncher
        """

        return self._launcher

    @property
    def progress_bar(self):
        """
        Returns updater progress bar
        :return: QProgressBar
        """

        return self._progress_bar

    @property
    def version(self):
        """
        Returns Artella launcher version
        :return: str
        """

        return self._version

    @property
    def envvar_name(self):
        """
        Returns the environment variable named used by updater to store installation path
        :return: str
        """

        return self._tools_env_var

    @property
    def progress_colors(self):
        """
        Returns progress colors
        :return: list(str)
        """

        return self._progress_colors

    @property
    def setup_url(self):
        """
        Returns path where setup.json file should be located in server
        :return: str
        """

        return '{}{}'.format(self._repository_url, self._last_version_file_name)

    def init_config(self):
        """
        Function that reads updater configuration and initializes launcher variables properly
        This function can be extended in new updaters
        """

        if not self.UPDATER_CONFIG_PATH or not os.path.isfile(self.UPDATER_CONFIG_PATH):
            artellalauncher.logger.error('Updater Configuration File for Artella Launcher not found! {}'.format(self.LAUNCHER_CONFIG_PATH))
            return

        with open(self.UPDATER_CONFIG_PATH, 'r') as f:
            updater_config_data = json.load(f)
        if not updater_config_data:
            artellalauncher.logger.error('Updater Configuration File for Artella Project is empty! {}'.format(self.LAUNCHER_CONFIG_PATH))
            return

        self._version = updater_config_data.get(defines.ARTELLA_CONFIG_UPDATER_VERSION, defines.DEFAULT_VERSION)
        self._tools_filename = updater_config_data.get(defines.UPDATER_TOOLS_FILE_ATTRIBUTE_NAME, "")
        self._tools_env_var = updater_config_data.get(defines.UPDATER_TOOLS_ENVIRONMENT_VARIABLE_ATTRIBUTE_NAME, '')
        self._repository_url = updater_config_data.get(defines.UPDATER_REPOSITORY_URL_ATTRIBUTE_NAME, "")
        self._last_version_file_name = updater_config_data.get(defines.UPDATER_LAST_VERSION_JSON_FILE_NAME, "")
        self._progress_colors.append(updater_config_data.get(defines.UPDATER_PROGRESS_BAR_COLOR_0_ATTRIBUTE_NAME, defines.DEFAULT_PROGRESS_BAR_COLOR_0))
        self._progress_colors.append(updater_config_data.get(defines.UPDATER_PROGRESS_BAR_COLOR_1_ATTRIBUTE_NAME, defines.DEFAULT_PROGRESS_BAR_COLOR_1))

        if not self._tools_env_var:
            self._tools_env_var = '{}_install'.format(self.launcher.get_clean_name())

    def get_default_installation_path(self, full_path=False):
        """
        Returns default installation path for tools
        :param full_path: bool
        :return: str
        """

        return ""

    def get_installation_path(self):
        """
        Returns tools installation path
        :return: str
        """

        try:
            if self.launcher.config:
                install_path = self.launcher.config.value(self.envvar_name)
            else:
                install_path = self.get_default_installation_path()
                self.launcher.config.setValue(self.envvar_name, install_path)
        except Exception:
            install_path = self.get_default_installation_path()
            if self.launcher.config:
                self.launcher.config.setValue(self.envvar_name, install_path)

        return install_path

    def set_installation_path(self):
        """
        Sets tools installation path
        """

        selected_dir = qtutils.get_folder(title='Select folder where you want to install {} tools'.format(self.launcher.name))
        if not selected_dir or not os.path.exists(selected_dir):
            qtutils.show_warning(None, 'Installation cancelled', '{} tools intallation cancelled!'.format(self.launcher.name))
            return

        return os.path.abspath(selected_dir)

    def get_tools_version(self):
        """
        :return:
        """

        pass

    def check_tools_version(self):
        """
        Checks the current installed version, returns True if the user don't have the last
        tools installed version or False otherwise.
        This function can be override in child updaters to implement specific functionality
        :return: bool, True if tools need to be updated or False otherwise
        """

        temp_path = tempfile.mkdtemp()
        install_path = self.get_installation_path()
        if install_path is None or not os.path.exists(install_path):
            self.launcher.console.write_error('> Installation path {} does not exists! Check that tools are installed in your system!\n'.format(install_path))
            return
        else:
            self.launcher.console.write('> Installation Path detected: {}\n'.format(install_path))
        QApplication.instance().processEvents()

        setup_path = path_utils.clean_path(os.path.join(temp_path, self._last_version_file_name))
        setup_file = self.setup_url

        self.launcher.console.write('> {} Tools Setup File: {}'.format(self.launcher.name.title(), setup_file))
        self.launcher.console.write('> {} Tools Setup Path: {}\n'.format(self.launcher.name.title(), setup_path))
        QApplication.instance().processEvents()

        if not download.download_file(filename=setup_file, destination=setup_path, console=self.launcher.console, updater=self):
            self.launcher.console.write_error('{} is not accessible! Maybe server is down. Try it later'.format(self._last_version_file_name))
            QApplication.instance().processEvents()
            return

        self.launcher.console.write('{} file downloaded successfully on {}\n'.format(setup_file, setup_path))
        QApplication.instance().processEvents()

        with open(setup_path, 'r') as f:
            setup_info = json.loads(f.read())

        last_version = setup_info.get('lastVersion')
        if not last_version:
            self.launcher.console.write_error('{} is not accessible! Maybe server is down or your internet connection is down! Try it later!')
            return
        self.launcher.console.write_ok('Last {} Tools deployed version is {}\n\n'.format(self.launcher.name.title(), last_version))

        tools_version_path = path_utils.clean_path(os.path.join(install_path, artellapipe.project.version_file_path))
        self.launcher.console.write('Checking current {} Tools installed version on {}'.format(self.launcher.name.title(), tools_version_path))
        QApplication.instance().processEvents()

        try:
            if os.path.isfile(tools_version_path):
                with open(tools_version_path, 'r') as f:
                    install_info = json.loads(f.read())
                installed_version = install_info.get('version')
                if not install_info:
                    self.launcher.console.write_error('Intsalled version impossible to get ...!')
                    return
                self.launcher.console.write_ok('\n\nCurrent installed version: {}\n'.format(installed_version))
                if installed_version == last_version:
                    self.launcher.console.write('\nCurrent installed {} Tools: {} are updated-to-date (version in server {})!'.format(self.launcher.name.title(), installed_version, last_version))
                    return False
                else:
                    return True
            else:
                return True
        except Exception as e:
            self.launcher.console.write_error('Error while retrieving {} Tools version!')
            self.launcher.console.write_error('{} | {}'.format(e, traceback.format_exc()))
            QApplication.instance().processEvents()
            return False

    def get_tools_version_status(self):
        """
        Returns information of the current version status
        :return: list(int, int, bool)
        """

        temp_path = tempfile.mkdtemp()
        install_path = self.get_installation_path()
        if install_path is None or not os.path.exists(install_path):
            return None, None, True

        setup_path = path_utils.clean_path(os.path.join(temp_path, self._last_version_file_name))
        setup_file = self.setup_url

        if not download.download_file(filename=setup_file, destination=setup_path, console=self.launcher.console, updater=self):
            return None, None, True

        with open(setup_path, 'r') as f:
            setup_info = json.loads(f.read())

        last_version = setup_info.get('lastVersion')
        if not last_version:
            return None, None, True

        tools_version_path = path_utils.clean_path(os.path.join(install_path, artellapipe.project.version_file_path))
        try:
            if os.path.isfile(tools_version_path):
                with open(tools_version_path, 'r') as f:
                    install_info = json.loads(f.read())
                installed_version = install_info.get('version')
                if not install_info:
                    return -1, -1, True
                if installed_version == last_version:
                    return last_version, installed_version, False
                else:
                    return last_version, installed_version, True
            else:
                return last_version, None, True
        except Exception as e:
            return last_version, None, True


    def update_tools(self):
        """
        Updates tools to the last available version
        """

        try:
            # temp_path = tempfile.mkdtemp()
            last_version, installed_version, need_to_update = self.get_tools_version_status()
            if need_to_update:
                install_path = self.get_installation_path()
                if install_path is None or not os.path.exists(install_path):
                    self.launcher.console.write_error('Install Path {} does not exists!'.format(install_path))
                    return
                else:
                    self.launcher.console.write('Install Path detected: {}'.format(install_path))
                QCoreApplication.instance().processEvents()

                self.launcher.console.write('=' * 15)
                self.launcher.console.write_ok('Current installed {} Tools are outdated {}!'.format(self.launcher.name.title(), installed_version))
                self.launcher.console.write_ok('Installing new tools ... {}!!'.format(last_version))
                self.launcher.console.write('=' * 15)
                QCoreApplication.instance().processEvents()
        except Exception as e:
            self.launcher.console.write_error('Error while updating {} Tools version!')
            self.launcher.console.write_error('{} | {}'.format(e, traceback.format_exc()))
            QApplication.instance().processEvents()
            return False


