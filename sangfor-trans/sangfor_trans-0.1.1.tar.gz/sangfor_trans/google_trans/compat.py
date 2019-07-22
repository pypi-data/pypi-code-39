# -*- coding: utf-8 -*-
import sys
try:
    # Python3  
    from urllib.parse import quote
except: 
    # Python2 
    from urllib import quote

# Python2和Python3兼容
PY3 = sys.version_info > (3, )

unicode = str if PY3 else unicode
