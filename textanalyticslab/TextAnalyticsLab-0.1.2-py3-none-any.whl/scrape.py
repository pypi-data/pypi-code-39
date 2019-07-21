# -*- coding: utf-8 -*-
# TextAnalytics (textanalytics)
__name__="mltk"
"""
TextAnalytics - a collection of text analytics tools for python.
===========================================================
'TextAnalytics' is a Python package providing a set of text analytics tools 
for data mining and machine learning projects and end-to-end text analytics 
application development. 

Author
------
- Sumudu Tennakoon

Links
-----
Website: http://sumudu.tennakoon.net/projects/TextAnalytics
Github: https://github.com/sptennak/TextAnalytics

License
-------
Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
"""

from datetime import datetime
import gc
import traceback
import gc
import os
import io
import requests
from timeit import default_timer as timer
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import warnings
warnings.filterwarnings("ignore")
from itertools import product, combinations, permutations, combinations_with_replacement
# More info on itertools https://docs.python.org/3.6/library/itertools.html

from bs4 import BeautifulSoup

def pandas_read_string(string, sep=',', header='infer', names=None, nrows=None, lineterminator=None, comment=None):
    """
    Convert string table to pandas dataframe
    """
    try:
        return pd.read_csv(io.StringIO(string), sep=sep, header=header, names=names, nrows=nrows, lineterminator=lineterminator, comment=comment)
    except:
        print('Error Converting String to DataFrame: {}'.format(traceback.print_exc()))
    return pd.DataFrame()
    
def find_pattern_webpage(targetPage, pattern):
    """
    Parameters
    ----------
    target_page : str, url
        URL of the target webpage
    pattern : str
		RegEx pattern
    Returns
    -------
    result : list(str)
        matching patterns found in the page
    """
    source = requests.get(targetPage).text
    soup = BeautifulSoup(source, 'lxml')
    text = soup.getText()
    try:
        result = re.search(pattern, text)
    except:
        result = None
    return result

def extract_tables_webpage(target_page):
    """
    Parameters
    ----------
    target_page : str, url
        URL of the target webpage

    Returns
    -------
    data_frames : list(pandas.DataFrame)
        list of pandas dataframes extracted
    """
    source = requests.get(target_page).text
    soup = BeautifulSoup(source, 'lxml')
    tableStr = soup.decode() #soup.findall('table').prettify() # Returns HTML table tag as a string
    data_frames = pd.read_html(tableStr) # Returns a list of dataframes from tables tags in the input string. header=0 is denote the first row conatins the column lables.
    return data_frames
	