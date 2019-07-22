#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import subprocess
import time

from .Trigger import Trigger


def loadSingleMulti(data, n):
    if n in data:
        if not isinstance(data[n], list):
            return([data[n]])
        else:
            return(data[n])
    return([])


class Rule:
    def __init__(self, tree, name, data, configdir, statusfile):
        self.tree = tree
        self.name = name
        self.cmd = loadSingleMulti(data, 'cmd')
        self.callBefore = loadSingleMulti(data, 'callBefore')
        self.callAfter = loadSingleMulti(data, 'callAfter')
        self.call = loadSingleMulti(data, 'call')
        self.configdir = configdir
        self.statusfile = statusfile
        self.trigger = [
            Trigger(t, self.configdir, self.statusfile) for
            t in loadSingleMulti(data, 'trigger')
        ]

    def show(self):
        print('name:', self.name)
        print('cmd:', self.cmd)
        print('callBefore:', self.callBefore)
        print('callAfter:', self.callAfter)
        print('call:', self.call)
        print('trigger:', self.trigger)
        print('-----')

    def run(self):
        run = False
        self.execCallBefore()
        if self.statusfile.checkRuleCallBefore(self.name, self.callBefore):
            run = True
        if not run:
            if self.checkTriggers():
                run = True
        if run:
            print(self.name)
            self.executeCmds()
            self.execCall()
            self.saveStatus()
            self.saveRunBeforeStatus()
        self.execCallAfter()
        return(run)

    def executeCmds(self):
        for c in self.cmd:
            subprocess.call('cd ' + self.configdir + '; ' + c,
                            shell=True, stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                            )

    def execCallBefore(self):
        for cb in self.callBefore:
            self.tree[cb].run()

    def execCallAfter(self):
        for ca in self.callAfter:
            self.tree[ca].run()

    def execCall(self):
        for c in self.call:
            self.tree[c].run()

    def checkTriggers(self):
        run = False
        if len(self.trigger) == 0:
            run = True
        for t in self.trigger:
            if t.eval():
                run = True
        return(run)

    def saveStatus(self):
        self.statusfile.setRule(self.name, time.time())

    def saveRunBeforeStatus(self):
        self.statusfile.saveRuleCallBefore(self.name, self.callBefore)
