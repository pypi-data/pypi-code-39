import re
import time
import glob
import Lace
import os,sys
import calendar
import datetime
import numpy as np
import pandas as pd
import xlwings as xw
from pathlib import Path
from openpyxl import load_workbook
from datetime import datetime as dt



prev_month = calendar.month_name[(dt.now().month)][:3] + dt.now().strftime("%Y")
curr_month1 = calendar.month_name[(dt.now().month+1)][:3] + dt.now().strftime("%Y")

if dt.now().month >= 9:
    annual_year = int(dt.now().strftime("%Y")) + 1
else:
    annual_year = int(dt.now().strftime("%Y"))
        
curr_process = curr_month1[:3].lower() + curr_month1[5:]


exec(open('netview_xlwings_version.py').read())


eperson2_path = r"\\nadayisicifs03.dayisi03.enterprisenet.org\share3\SRData\UEData\NielsenOnlineHomeUEs/"
eperson2_path = output_path
print('\n\n#################################################################')
print("Path for ePerson2+ input file:\n ",eperson2_path)
print('#################################################################')



annual_update_path = r"\\nadayisicifs03.dayisi03.enterprisenet.org\share3\SRData\UEData\Internet UEs\Annual Update_{0}".format(annual_year)
print('\n\n#################################################################')
print("\npath for Annual weights input file:\n ",annual_update_path)
print('#################################################################')



exec(open('any_wings.py').read())

exec(open('total.py').read())
