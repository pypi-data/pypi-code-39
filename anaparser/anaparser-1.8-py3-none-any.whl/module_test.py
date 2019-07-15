#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 14:50:38 2019

@author: deniszagorodnev
"""

import anaplan_parser as ap

fname = 'М30.34 Затраты на возобновление CAPEX СМК Отчет.xls'


Input_path = '/Users/deniszagorodnev/Desktop/'
Output_path = '/Users/deniszagorodnev/Desktop/anaplan_parse/'

parser = ap.file_parser(Input_path = Input_path, Output_path = Output_path)

parser.parse_file(fname)
