#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from .Rule import Rule


class RulesTree:
    def __init__(self, data, configdir):
        self.data = data['rules']
        self.configdir = configdir
        self.rules = {}
        self.load()

    def load(self):
        for n, r in self.data.items():
            self.rules[n] = Rule(self, n, r, self.configdir)

    def __getitem__(self, n):
        return(self.rules[n])
