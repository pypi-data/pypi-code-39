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

def normalize_text(text, method='str'):  
    """
    Parameters
    ----------
    text : str
    method : {'str', 'regex'}, default 'str'
        str: cleans digits and puntuations only ('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
        regex : clean digits and all special characters 
        
    Returns
    -------
    text : str
    """
    
    # Conver to lower case
    text = text.lower()
        
    if method=='str':    
        # Remove digits
        text = ''.join(c for c in text if not c.isdigit())            
        # Remove punctuation
        from string import punctuation   
        text = ''.join(c for c in text if c not in punctuation)        
        # Remove extra spaces
        text = " ".join(text.split())
    
    elif method=='regex':
        import re
        # Remove digits
        text = re.sub(r'\d+', ' ', text) 
        # Remove all special characters
        text = re.sub(r'\W+', ' ', text) 
        # Remove extra spaces
        text = re.sub('\s\s+', ' ', text)
        
    return text
	
def remove_quoted_printable_encoding(Text):
    #Quoted-Printable Content-Transfer-Encoding
    #Source: http://www.freesoft.org/CIE/RFC/1521/6.htm  
	#https://www.w3.org/Protocols/rfc1341/5_Content-Transfer-Encoding.html
	#https://stackoverflow.com/questions/25710599/content-transfer-encoding-7bit-or-8-bit
    QPCTE = {
            '= '    :' ', #Soft line break (ignore).
            '==09'  :'', #Soft line break (ignore).
            '==20'  :' ', #Soft line break (ignore).  
            '=\t'  :'\t', #Soft line break (ignore). 
            '=\n'  :'', #Soft line break (ignore). 			
            '=09'   :'\t',  
            '=0A'   :'\n',
            '=0C'   :'\f', 
            '=0D'   :'\r',
            '=0D=0A':'\r\n',
            '=20'   :' ',  #Space   
            '=21'   :'!',  
            '=22'   :'"',  
            '=23'   :'#',  
            '=24'   :'$',          
            '=25'   :'%',          
            '=26'   :'&', 
            '=27'   :"'",  
            '=28'   :'(',  
            '=29'   :')',  
            '=2A'   :'*', 
            '=2B'   :'+',  
            '=2C'   :',',  
            '=2D'   :'-',        
            '=2E'   :'.', 
            '=2F'   :'/', 
            '=3A'   :':', 
            '=3B'   :';', 
            '=3C'   :'<', 
            '=3D'   :'=',
            '=3E'   :'>', 
            '=3F'   :'?',
            '=85'   :'...',
            '=91'   :"'",
            '=92'   :"'",
            '=93'   :'"',
            '=94'   :'"',
            '=95'   :u'\x95',
            '=96'   :'-',
            '=97'   :'--',
            '=98'   :'~',
            '=99'   :u'\x99',  #TM
            '=A9'   :u'\xA9',  #Copyright
            '=AE'   :u'\xAE',   #Registered
            '=E0'   :u'\xE0',
            '=E1'   :u'\xE1',
            '=E2'   :u'\xE2',
            '=E3'   :u'\xE3',   
            '=E4'   :u'\xE4', 
            '=E8'   :u'\xE8', 
            '=E9'   :u'\xE9', 
            '=EA'   :u'\xEA', 
            '=EB'   :u'\xEB',
            '=EC'   :u'\xEC',
            '=ED'   :u'\xED',
            '=EE'   :u'\xEE',
            '=F1'   :u'\xF1',
            '=F2'   :u'\xF2',
            '=F3'   :u'\xF3',   
            '=F4'   :u'\xF4',        
            '=F5'   :u'\xF5',  
            '=F6'   :u'\xF6',
            '=F7'   :u'\xF7',
            '=F8'   :u'\xF8',   
            '=F9'   :u'\xF9',        
            '=FA'   :u'\xFA', 
            '=FB'   :u'\xFB', 
            '=FC'   :u'\xFC', 
            '=FD'   :u'\xFD', 
            }

    for (pattern,replacement) in QPCTE.items():
        Text = Text.replace (pattern, replacement)  
    
    return Text
        
    
def remove_html_tags(Text):
    # apply rules in given order!
    rules =  [
            { r'[\x20][\x20]+' : u' '},                   # Remove Consecutive spaces
            { r'\s*<br\s*/?>\s*' : u'\n'},      # Convert <br> to Newline 
            { r'</(p|h\d)\s*>\s*' : u'\n\n'},   # Add double newline after </p>, </div> and <h1/>
            { r'<head>.*<\s*(/head|body)[^>]*>' : u'' },     # Remove everything from <head> to </head>
            { r'<script>.*<\s*/script[^>]*>' : u'' },     # Remove evrything from <script> to </script> (javascipt)
            { r'<style>.*<\s*/style[^>]*>' : u'' },     # Remove evrything from <style> to </style> (stypesheet)
            { r'<[^<]*?/?>' : u'' },            # remove remaining tags
            #{ r'<[^>]+>' : u''}
            ]
     
    for rule in rules:
        for (pattern,replacement) in rule.items():
            Text  = re.sub (pattern, replacement, Text)
			
    return Text
	
def parse_html_entities(text):            
    #https://www.w3schools.com/charsets/ref_html_entities_4.asp
    #https://docs.python.org/3/library/html.entities.html#html.entities.html5     
    enities={
                'cent;'   :u'\xA2',
                '&pound;' :u'\xA3',
                '&copy;'  :u'\xA9',
                '&reg;'   :u'\xAE',
                '&plusmn;':u'\xB1',
                '&frac14;':u'\xBC',
                '&frac12;':u'\xBD',
                '&frac34;':u'\xBE',
                '&times;' :u'\xD7',
                '&prime;' :u'\x2032',
                '&Prime'  :u'\x2033',
                '&lowast;':u'\x2217',
                '&ne;'    :u'\x2260',
                '&trade;' :u'\x2122',
                '&#8211;' :u'\x8211',
                '&#8217;' :u'\x8217',
                '&amp;'   :'&',
				}

    for (pattern,replacement) in enities.items():
        text = text.replace (pattern, replacement)  

    return text
        
def remove_consecutive_whitespace(text):
    """
	Preserve line breaks and tabs
    """
    text=re.sub('[\x20][\x20]+' , ' ', text)
    text=re.sub('[\n][\n]+' , '\n', text)
    text=re.sub('[\t][\t]+' , '\t', text)
    text=re.sub('[\r][\r]+' , '\r', text)
    return text