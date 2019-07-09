#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import json
import os


class Trigger:
    def __init__(self, configdir, triggerconfig):
        self.configdir = configdir
        self.triggerconfig = triggerconfig
        self.triggerstatus = TriggerStatus(
            os.path.abspath(
                os.path.join(self.configdir, 'awesomestatus.json')
            )
        )
        self.value = self.triggerconfig['value']
        self.eval, ispath = {
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
        if ispath:
            self.relpath = self.value
            self.abspath = os.path.abspath(
                os.path.join(self.configdir, self.value)
            )

    def fileChangedTrigger(self):
        ts = self.triggerstatus[self.relpath]
        if not os.path.isfile(self.abspath):
            return(True)
        cs = os.popen('cat ' + self.abspath + ' | sha512sum').read()
        self.triggerstatus[self.relpath] = cs
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
        ts = self.triggerstatus[self.relpath]
        if not os.path.isdir(self.abspath):
            return(True)
        cs = os.popen(
            'cd ' + self.configdir
            + '; ls -RlgAGi --time-style=+%s '
            + self.relpath + ' | sha512sum'
        ).read()
        self.triggerstatus[self.relpath] = cs
        if ts is None:
            return(True)
        if ts != cs:
            return(True)
        return(False)

    def directoryexistTrigger(self):
        return(os.path.isdir(self.abspath))

    def directoryNotexistTrigger(self):
        return(not os.path.isdir(self.abspath))


class TriggerStatus:
    def __init__(self, path):
        self.abspath = path

    def __getitem__(self, key):
        if os.path.isfile(self.abspath):
            with open(self.abspath) as json_file:
                data = json.load(json_file)
            if key in data:
                return(data[key])
        return(None)

    def __setitem__(self, key, value):
        data = {}
        if os.path.isfile(self.abspath):
            with open(self.abspath) as json_file:
                data = json.load(json_file)
        data[key] = value
        with open(self.abspath, 'w') as json_file:
            json.dump(data, json_file, indent=4, sort_keys=True)
