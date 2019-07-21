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
from timeit import default_timer as timer
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import warnings
warnings.filterwarnings("ignore")
from itertools import product, combinations, permutations, combinations_with_replacement
# More info on itertools https://docs.python.org/3.6/library/itertools.html

import re

EMAIL_FORMAT = re.compile(r"([a-zA-Z0-9!#$%&'\*\+\-/=?^_`{|}~,][a-zA-Z0-9!#$%&'\*\+\-\./=?^_`{|}~,]{1,63}@[\w\.-]{1,253}\.[\w\.-]{1,63})")
EMAIL_DOMAIN_FORMAT = re.compile(r'@([\w\.-]{1,253}\.[\w\.-]{1,63})')
PHONENUM_FORMAT = re.compile(r'(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$')

def extract_email_addresses(text):
    return re.findall(EMAIL_FORMAT, text)

def extract_email_domains(text):
    #https://en.wikipedia.org/wiki/Email_address
    #local-part@domain-part (max. 64@255 characters)
    return re.findall(EMAIL_DOMAIN_FORMAT, text)

def extract_phone_number(text):
    return re.findall(PHONENUM_FORMAT, text)
	
def split_upc(Code):
    #https://en.wikipedia.org/wiki/Universal_Product_Code
    Code = re.sub('[^0-9]+', '', Code) #Cleanup the code
    SystemDigit = Code[0]
    CheckDigit = Code[-1]
    #######################################################################
    LLLLL = Code[1:6] #LLLLL is the item number, and the , with the 
    RRRRR = Code[-6:-1] #RRRRR is either the weight or the price
    R1 = Code[-6] #first R determining which (0 for weight)
    #######################################################################
    RRR_ = Code[-6:-3] # LLLLL digits are the manufacturer code, the first three RRR are a family code (set by manufacturer)
    _RR = Code[-3:-1] #last 2 digits: coupon code, which determines the amount of the discount
    #######################################################################
    LR10 = Code[1:-1] # National Drug Code (NDC). (UPN Codes)
    
    return {'SystemDigit':SystemDigit, 'CheckDigit':CheckDigit , 'LLLLL':LLLLL, 'RRRRR':RRRRR, 'R1':R1, 'RRR_':RRR_, 'LR10':LR10}

def upc_check_digit(Code):
    #https://en.wikipedia.org/wiki/Universal_Product_Code
    Code = re.sub('[^0-9]+', '', Code) #Cleanup the code

    DigitCount = len(Code)
    
    if DigitCount==12:
        #######################################################################
        CheckFormula=np.array([3,1,3,1,3,1,3,1,3,1,3,1])
        Digits = np.zeros(DigitCount, dtype=np.int)
        for i in range(DigitCount-1):
            Digits[i] = int(Code[i])
        M = np.sum(Digits*CheckFormula) % 10
        if M != 0:
            CheckDigitValue = 10 - M
        else:
            CheckDigitValue = 0
        #######################################################################
    else:
        CheckDigitValue = -1
        
    return CheckDigitValue
 
def check_upc(Code):
    CheckDigitValue = upc_check_digit(Code)
    if CheckDigitValue==int(Code[-1]):
        return True
    else:
        return False