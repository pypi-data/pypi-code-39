#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import os

from .TriggerStatus import TriggerStatus


class Trigger:
    def __init__(self, triggerconfig, configdir, statusfile):
        self.configdir = configdir
        self.triggerconfig = triggerconfig
        self.value = self.triggerconfig['value']
        self.statusfile = statusfile
        self.eval, self.ispath = {
            'file': {
                'changed': (self.fileChangedTrigger, True),
                'exist': (self.fileexistTrigger, True),
                'not exist': (self.fileNotexistTrigger, True)
            },
            'directory': {
                'changed': (self.directoryChangedTrigger, True),
                'exist': (self.directoryexistTrigger, True),
                'not exist': (self.directoryNotexistTrigger, True)
            }
        }[self.triggerconfig['type']][self.triggerconfig['subtype']]
        if self.ispath:
            self.relpath = self.value
            self.abspath = os.path.abspath(
                os.path.join(self.configdir, self.value)
            )
        self.triggerstatus = TriggerStatus(self)

    def fileChangedTrigger(self):
        ts = self.triggerstatus.get()
        if not os.path.isfile(self.abspath):
            return(True)
        cs = os.popen('cat ' + self.abspath + ' | sha512sum').read()
        self.triggerstatus.set(cs)
        if ts is None:
            return(True)
        if ts != cs:
            return(True)
        return(False)

    def fileexistTrigger(self):
        return(os.path.isfile(self.abspath))

    def fileNotexistTrigger(self):
        return(not os.path.isfile(self.abspath))

    def directoryChangedTrigger(self):
        ts = self.triggerstatus.get()
        if not os.path.isdir(self.abspath):
            return(True)
        cs = os.popen(
            'cd ' + self.configdir
            + '; ls -RlgAGi --time-style=+%s '
            + self.relpath + ' | sha512sum'
        ).read()
        self.triggerstatus.set(cs)
        if ts is None:
            return(True)
        if ts != cs:
            return(True)
        return(False)

    def directoryexistTrigger(self):
        return(os.path.isdir(self.abspath))

    def directoryNotexistTrigger(self):
        return(not os.path.isdir(self.abspath))
