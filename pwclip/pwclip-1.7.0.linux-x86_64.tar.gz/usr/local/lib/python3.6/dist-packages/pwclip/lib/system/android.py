#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is free software by d0n <d0n@janeiskla.de>
#
# You can redistribute it and/or modify it under the terms of the GNU -
# Lesser General Public License as published by the Free Software Foundation
#
# This is distributed in the hope that it will be useful somehow.
# !WITHOUT ANY WARRANTY!
#
# Without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
from re import sub
from subprocess import run

def adbenter():
	run('%s shell input keyevent 66'%which('adb'), shell=True)

def adbout(text, enter=None):
	adb = which('adb')
	text = sub(r'(\s|\$|\%|\&|\(|\)|\=|\?|\-|\!|\+|\.)', r'\\\1', text)
	text = sub(r'"', r'\\\\\"', text)
	text = sub(r"'", r"\'", text)
	run(r'%s shell input text "%s"'%(adb, r'%s'%text), shell=True)
	if enter:
		adbenter()
