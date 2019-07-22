#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import glob
import json
import os


def importrules(data, configdir):
    importrules = []
    if 'import' in data:
        if isinstance(data['import']['rules'], dict):
            importrules = data['import']['rules']
        else:
            importrules += data['import']['rules']
    for ir in importrules:
        irr = {}
        ipath = os.path.abspath(os.path.join(configdir, ir['value']))
        if ir['type'] == 'directory':
            for irf in glob.glob(ipath + '/*.json'):
                with open(irf) as json_file:
                    irr.update(json.load(json_file))
        if ir['type'] == 'file':
            with open(ipath) as json_file:
                irr = json.load(json_file)
        if ir['rules'] == '*':
            data['rules'].update(irr)
        else:
            for irrl in ir['rules']:
                data['rules'][irrl] = irr[irrl]
    return(data)
