# -*- coding: utf-8 -*-
"""
cakemix
~~~~~

Cakemix is a Python library to make the business life easier. It uses standard Python libraries and simplifies opening/writing excel spreadsheets, 
comparing data in several spreadsheets, making ppt files, to reading pdf files.
It also has functions to automate the routine work like emailing, sending
reminders.

:copyright: © 2019 by Mesut Varlioglu, PhD.
:license: BSD, see LICENSE.rst for more details.
"""

#List classes
from .list import findUniqueList

#Web classes
from .web import openURL, getLinks

#Excel classes
from .excel import readExcel, plotBarData, plotHistData, plotLineData, plotScatterData






name = "cakemix"
__version__ = '0.0'
