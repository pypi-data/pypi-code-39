#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) Smart Arcs Ltd, registered in the United Kingdom.
# This file is owned exclusively by Smart Arcs Ltd.
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
import sys

__copyright__ = 'Smart Arcs Ltd'
__email__ = 'support@smartarchitects.co.uk'
__status__ = 'Development'

import os
import os.path


# noinspection PyBroadException
class Core(object):
    """
    Pidlock + configuration
    """

    CONFIG_DIR = '.'
    try:
        CONFIG_DIR = os.environ['KC_CONFIG_DIR']
    except Exception:
        # hopefully just the key is not set
        CONFIG_DIR = os.path.expanduser("~/.keychest")
        try:
            _path = os.path.join(CONFIG_DIR)
            if not os.path.exists(_path):
                os.makedirs(_path, mode=0o755)

        except Exception as ex:
            CONFIG_DIR = os.path.expanduser("~")

    @classmethod
    def clear_pid(cls):
        pid_file = os.path.join(os.path.join(Core.CONFIG_DIR, 'var/run'), "keychest_agent.pid")
        # my_pid = "%s" % os.getpid()
        if os.path.exists(pid_file):
            os.remove(pid_file)

    def __init__(self):
        """Init the core functions"""

        pid_file = os.path.join(os.path.join(Core.CONFIG_DIR, 'var/run'), "keychest_agent.pid")
        my_pid = "%s" % os.getpid()
        if os.path.exists(pid_file):
            with open(pid_file, 'r') as f:
                file_pid = f.read()
            if file_pid != my_pid:
                sys.stderr.write("There is a running agent with process id %s" % open(pid_file, 'r').read())
                exit(-1)
        else:
            if not os.path.exists(os.path.join(Core.CONFIG_DIR, 'var/run')):
                os.makedirs(os.path.join(Core.CONFIG_DIR, 'var/run'), mode=0o755)
            f = open(pid_file, 'w')
            f.write("%r" % os.getpid())
            f.close()
        try:
            _path = os.path.join(Core.CONFIG_DIR, 'var/run')
            if not os.path.exists(_path):
                os.makedirs(_path, mode=0o755)
        except:
            sys.stderr.write("Can't create a config folder '<base_path>/var/run'\n")

        self.pidlock_created = False

    @classmethod
    def get_custom_config_file_path(cls, filename):
        """Returns configuration file for my own file"""
        return os.path.join(Core.CONFIG_DIR, filename)

    # def pidlock_create(self):
    #     """
    #     Creates a new pidlock if it was not yet created
    #     :return:
    #     """
    #     if not self.pidlock_created:
    #         self.pidlock.create()
    #         self.pidlock_created = True

    # def pidlock_check(self):
    #     """
    #     Checks if the current process owns the pidlock
    #     :return: True if the current process owns the pidlock
    #     """
    #     return self.pidlock.check()

    # def pidlock_get_pid(self):
    #     """
    #     Returns pid of the process holding pidlock, None if there is none.
    #     :return:
    #     """
    #     filename = self.pidlock.filename
    #     if filename and os.path.isfile(filename):
    #         try:
    #             with open(filename, "r") as fh:
    #                 fh.seek(0)
    #                 _pid = int(fh.read().strip())
    #                 return _pid
    #         except:
    #             pass
    #
    #     return None
