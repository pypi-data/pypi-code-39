#################################################################
'''
	This is US Netview process for the non major month.
	If you are running the process for the month of March
	Please make sure the Start date of Julian Calendar
	doesn't fall between the previous year and the current year
	If it does, need to uncomment the codes from 148 to 152
	and make the adjustment before running the code.
'''
#################################################################

print("Enter the Destination address:")
destination = str(input())
# r"C:\Users\anal8003\Desktop\GOT\US netview UE non major\mar19"
print("Enter the Run directory where the codes are there:")
run_dir = str(input())
# r"C:\Users\anal8003\Desktop\GOT\us_netview\Home_UE"

#########################################

#           Import Packages

#########################################

import time
import pickle
import ftplib
import sys, os
import datetime
import calendar
import numpy as np
import pandas as pd
from pathlib import Path
from itertools import chain
from datetime import datetime as dt
os.chdir(run_dir)
import Lace

#################################################

# Calculating quarter for Major and Non major months

#################################################

period = ["jan", "apr", "jul", "oct"]

month = calendar.month_abbr[datetime.datetime.now().month+1].lower()+str(datetime.datetime.now().year+1 if datetime.datetime.now().month+1 >= 12 else datetime.datetime.now().year)[2:]  # current processing month
print("\n################################################################\n")
print("\nThe entered the current processing month:", month)
print("\n################################################################\n")
tam_period = {"feb":["feb","mar","apr"],
              "may":["may","jun"],
              "jul":["jul","aug","sep"],
              "oct":["oct"],
              "nov":["nov","dec","jan"]}

def rest_month(month):
    v = [k for (k, v) in tam_period.items() if month in v]
    current_quarter = v[0] if len(v) > 0 else month.title()
    return current_quarter+str(datetime.datetime.now().year+1 if datetime.datetime.now().month+1 >= 12 else datetime.datetime.now().year)[2:]

TAM_sync = rest_month(month[:3])

print("\n################################################################\n")
print("\nThe enter the prior TAM sync:", TAM_sync)
print("\n################################################################\n")
 
#######################################################################

# Automation to calculate Julian dates, TGB2 file names  

#######################################################################
      
def tgb2_file(filename1, filename2=None):
    '''
	This function takes the string values and julian dates
	from julian_dates() function and give the output as
		1. List of TGB2 file 
		2. Start date of Julian date
		3. Ending date for Julian date
	According to the number of TGB2 files used
	 '''
    if filename2 == None:
        tgb2_1stmonth = filename1
        day1 = julian_dates()[0] - 1
        bday1 = 1
        eday1 = 28
        return [tgb2_1stmonth], day1, bday1, eday1
    elif filename2 != None:
        tgb2_1stmonth = filename1
        tgb2_2ndmonth = filename2
        day1 = julian_dates()[0] - 1
        bday1 = 29
        eday1 = 35
        day2 = julian_dates()[0] + 6
        bday2 = 1
        eday2 = 21
        return [tgb2_1stmonth, tgb2_2ndmonth], day1, bday1, eday1, day2, bday2, eday2
      
def julian_dates():
    '''
	This function calculate Julian dates by 
	counting previous Nine weeks and give the
	starting Julian date for the proces
	Output are
		1. Julian date
		2. Year
		3. month
	'''
    year = datetime.datetime.now().year
    j_curr = datetime.datetime.now().month
    j_prev = j_curr - 2
    if j_prev == 0: 
        p_year = year -1 
        j_prev = datetime.datetime(p_year,12,1).month
    elif j_prev == -1:
        p_year = year -1 
        j_prev = datetime.datetime(p_year,11,1).month
    elif j_prev == -2:
        p_year = year -1 
        j_prev = datetime.datetime(p_year,10,1).month
    else:
        p_year = year
        j_prev = j_prev

    if (year%4 == 0)&(j_prev == 2):
        d = len(calendar.monthcalendar(p_year,j_prev))-1
        start_julian = calendar.monthcalendar(p_year,j_prev)[d][0]
    else:
        if calendar.monthcalendar(year,j_curr)[0][0] == 0:
            start_julian = calendar.monthcalendar(p_year,j_prev)[-1][0]
        elif calendar.monthcalendar(year,j_curr)[0][0] != 0:
            start_julian = calendar.monthcalendar(p_year,j_prev)[-1][0]
        else:
            start_julian

    julian = datetime.datetime(p_year, j_prev, start_julian)    
    julian_tuple = julian.timetuple()
    return (int(str(julian_tuple.tm_year)[2:] + "{:03d}".format(julian_tuple.tm_yday)),p_year,j_prev)

def tgb2_name(julian_dates,j_year,prev_month):
    '''
	This function takes the input from julian_dates() function
	and return the number of TGB2 files used for the process,
	year and month.
    '''
    if (calendar.monthcalendar(j_year,prev_month)[-1][-1] == 0) & (calendar.monthcalendar(j_year,prev_month)[-1][-2] != 0) & (prev_month == 8):
        number = 1
        j_prev = 1 if prev_month >= 12 else prev_month+1
    elif (calendar.monthcalendar(j_year,prev_month)[-1][-1] >= 29) & (calendar.monthcalendar(j_year,prev_month)[-1][-2] != 0):
        number = 2
        j_prev = prev_month
    elif (calendar.monthcalendar(j_year,prev_month)[-1][-2] != 0) & (calendar.monthcalendar(j_year+1 if prev_month >= 12 else j_year,1 if prev_month >= 12 else prev_month+1)[0][-1] == 1):
        number = 1
        j_prev = 1 if prev_month >= 12 else prev_month+1
    elif calendar.monthcalendar(j_year,prev_month)[-1][-2] == 0 :
        number = 1
        j_prev = 1 if prev_month >= 12 else prev_month+1
    
    return number, j_year, j_prev
    
number, j_year, j_prev = tgb2_name(julian_dates()[0], julian_dates()[1], julian_dates()[2])
    
if number == 1:
    tgb2_1stmonth = 'tgb2.'+calendar.month_abbr[j_prev].lower()+str(j_year+1 if julian_dates()[2] >= 12 else j_year)[2:]
    print("\n*******************************\n")
    print(tgb2_1stmonth,"\nThese are TGB2 file used for the processing month")
    print("\n*******************************\n")
    response = input("\n Are sure you want use these:\n")
    if response == 'yes':
        file_list2, day1, bday1, eday1 = tgb2_file(tgb2_1stmonth)
    elif response == 'no':
        tgb2_1stmonth = input("\n Please enter the TGB2 file you wish to use:\n")
        file_list2, day1, bday1, eday1 = tgb2_file(tgb2_1stmonth)
elif number == 2:
    tgb2_1stmonth = 'tgb2.'+calendar.month_abbr[j_prev].lower()+str(j_year)[2:]
    j_prev = 1 if j_prev >= 12 else j_prev+1
    tgb2_2ndmonth = 'tgb2.'+calendar.month_abbr[j_prev].lower()+str(j_year )[2:]
    print("\n*******************************\n")
    print(tgb2_1stmonth,tgb2_2ndmonth,"\nThese are TGB2 file used for the processing month")
    print("\n*******************************\n")
    response = input("\n Are sure you want use these:\n")
    if response == 'yes':
        file_list2, day1, bday1, eday1, day2, bday2, eday2 = tgb2_file(tgb2_1stmonth, tgb2_2ndmonth)
    elif response == 'no':
        tgb2_1stmonth = input("\n Please enter the first TGB2 file you wish to use:\n")
        tgb2_2ndmonth = input("\n Please enter the second TGB2 file you wish to use:\n")
        file_list2, day1, bday1, eday1, day2, bday2, eday2 = tgb2_file(tgb2_1stmonth, tgb2_2ndmonth)

###################################################################################################

server = "cvgsolsasp001"
user = "anal8003"
password = "wrekLST9"
source1 = "/home/jcl/internet/data/restore/"
source2 = '/auto/acn/nti/data/tgb2/'
source3 = '/auto/acn/ueda/data/meterwtg/Internet/'
source4 = "/home/jcl/internet/data/"
source5 = "/auto/acn/ueda/data/meterwtg/" + TAM_sync + '/'
interval = 0.05

file_list1 = ['ustotue.sas7bdat', 'apmmvremue.sas7bdat', 'apmmvremuep2p.sas7bdat',
              'dmaue.sas7bdat']

cat = ['hhinpapvrm', 'reg', 'hhsz', 'ed', 'hisp', 'hoh', 'ch16', 'pers', 'hisp', 'ed']

##############################################################################

# For Four Major month

#############################################################################
def quarter(month):
    if month in [1, 2, 12]:
        # quarter = 'jan' + str(dt.now().year)[-2:]
        per1 = [i + str(dt.now().year)[-2:] for i in period[:1]] + [i + str(int(str(dt.now().year)[-2:]) - 1) for i in
                                                                    period[1:]]
    elif month in [3, 4, 5]:
        # quarter = 'apr' + str(dt.now().year)[-2:]
        per1 = [i + str(dt.now().year)[-2:] for i in period[:2]] + [i + str(int(str(dt.now().year)[-2:]) - 1) for i in
                                                                    period[2:]]
    elif month in [6, 7, 8]:
        # quarter = 'jul' + str(dt.now().year)[-2:]
        per1 = [i + str(dt.now().year)[-2:] for i in period[:3]] + [i + str(int(str(dt.now().year)[-2:]) - 1) for i in
                                                                    period[3:]]
    elif month in [9, 10, 11]:
        # quarter = 'oct' + str(dt.now().year)[-2:]
        per1 = [i + str(dt.now().year)[-2:] for i in period]
    return per1


per1, per2, per3, per4 = quarter(dt.now().month)
periods = [per1, per2, per3, per4]

for i in cat[:1]:
    for j in periods:
        file_list1.append(str(i) + str(j) + '.sas7bdat')

for i in cat[1:8]:
    for j in periods:
        file_list1.append(str(i) + 'pct' + str(j) + '.sas7bdat')
    file_list1.append(str(i) + 'ue.sas7bdat')

for i in cat[7:]:
    for j in periods:
        file_list1.append(str(i) + 'pctp2p' + str(j) + '.sas7bdat')
    file_list1.append(str(i) + 'uep2p.sas7bdat')

for j in periods:
    file_list1.append('dmapct' + str(j) + '.sas7bdat')
    file_list1.append('dmapctp2p' + str(j) + '.sas7bdat')

file_list3 = ['wts.natl.' + month, 'wts.Remainder.'+month ,'wts.Remainder', 'wts.national']

ftp = ftplib.FTP(server)
ftp.login(user, password)


def downloadFiles(path, destination, filelist):
    try:
        ftp.cwd(path)
        os.chdir(destination)
        os.makedirs(destination + "\Input")
        print("Created: " + destination + "\Input")
    except OSError:
        pass
    except ftplib.error_perm:
        print("Error: could not change to " + path)
        sys.exit("Ending Application")

    for file in filelist:
        time.sleep(interval)
        try:
            ftp.cwd(path + file + "/")
            downloadFiles(path + file + "/", destination)
        except ftplib.error_perm:
            os.chdir(destination + "\Input")

            try:
                ftp.retrbinary("RETR " + file, open(os.path.join(destination + "\Input", file), "wb").write)
                print("Downloaded: " + file)
            except:
                print("Error: File could not be downloaded " + file)
    return


downloadFiles(source1, destination, file_list1)
downloadFiles(source2, destination, file_list2)
downloadFiles(source5, destination, file_list3[2:])
downloadFiles(source3, destination, file_list3[:2])
downloadFiles(source1, destination, list(['wwts' + str(TAM_sync) + 'rem.sas7bdat']))
downloadFiles(source1, destination, list(['agesex' + str(TAM_sync) + '.sas7bdat']))

files = Path(destination) / 'Input'
file_dir = os.listdir(files)
os.mkdir(Path(files) / "Avg")

for file in file_dir:
    try:
        if file.endswith('.sas7bdat'):
            read_file = pd.read_sas(Path(files) / file, encoding='utf-8')
            excel_file = 'Avg/' + file.split('.')[0] + ".csv"
            print(Path(files) / excel_file)
            read_file.to_csv(Path(files) / excel_file, index=False)
    except:
        pass
# read_file = pd.read_sas(Path(files)/'agesexjan19.sas7bdat',encoding='utf-8')
# read_file.to_csv(Path(files)/'agesexjan19.csv',index=None)

# Update path for program folder
path = destination
os.chdir(path)

# Create a folder 'Input' and keep all the input files in it
inpath = path + '\\Input\\'

period = month
os.chdir(run_dir)

#############################################################################################

# ----------------------------------------------------------------------------
#                               tgb2.py
# ----------------------------------------------------------------------------


if number == 1:
    infile1 = file_list2[0]
    exec(open('tgb2_1month.py').read())
elif number == 2:
    infile1 = file_list2[0]
    infile2 = file_list2[1]
    exec(open('tgb2.py').read())

# Output:
#    "tgb2forMMMYY.pkl" - Used as a input for next programs
#    "agesexMMMYY.pkl" - Used as a input for next programs
#    "Tgb2_Output_num.xlsx" - Numbers are used in excel templates


# ----------------------------------------------------------------------------
#                               mosumwts.py
# ----------------------------------------------------------------------------

exec(open('mosumwts.py').read())

# ----------------------------------------------------------------------------
#                               uscontrols.py
# ----------------------------------------------------------------------------
#    Files are available in the path - /home/jcl/internet/data/restore
#    Below files needs to be converted from SAS to excel
#    Converted files needs to be placed in the 'Input' Folder


ustotue = pd.read_csv(inpath + 'Avg/ustotue.csv')
apmmvremue = pd.read_csv(inpath + 'Avg/apmmvremue.csv')
apmmvremuep2p = pd.read_csv(inpath + 'Avg/apmmvremuep2p.csv')

exec(open('uscontrols.py').read())

# ----------------------------------------------------------------------------
#                               sumwts.py
# ----------------------------------------------------------------------------

exec(open('remwts.py').read())

# ----------------------------------------------------------------------------
#                               sumwts.py
# ----------------------------------------------------------------------------
vars()['agesex' + str(TAM_sync)] = pd.read_csv(inpath + 'Avg/' + 'agesex' + str(TAM_sync) + '.csv')
# vars()['hhinpapvrm'+str(per1)]=pd.read_csv(inpath+'Avg/' + 'agesex'+str(per1)+'.csv')
vars()['wwts' + str(TAM_sync) + 'rem'] = pd.read_csv(inpath + 'Avg/' + 'wwts' + str(TAM_sync) + 'rem.csv')

exec(open('sumwts.py').read())

# ----------------------------------------------------------------------------
#                               moapmmvrem.py
# ----------------------------------------------------------------------------

exec(open('moapmmvrem.py').read())

# ----------------------------------------------------------------------------
#                               avg4lac.py
# ----------------------------------------------------------------------------


#    Below files needs to be converted from SAS to excel
#    Files are available in the path - /home/jcl/internet/data/restore
#    Create a folder 'Avg' and keep all below files in it 

ms = ['reg', 'hhsz', 'ed', 'hisp', 'hoh', 'ch16']

for i in ms:
    vars()[str(i) + 'pct' + str(per1)] = pd.read_csv(inpath + 'Avg/' + str(i) + 'pct' + str(per1) + '.csv')
    vars()[str(i) + 'pct' + str(per3)] = pd.read_csv(inpath + 'Avg/' + str(i) + 'pct' + str(per3) + '.csv')
    vars()[str(i) + 'pct' + str(per4)] = pd.read_csv(inpath + 'Avg/' + str(i) + 'pct' + str(per4) + '.csv')
    vars()[str(i) + 'pct' + str(per2)] = pd.read_csv(inpath + 'Avg/' + str(i) + 'pct' + str(per2) + '.csv')
    vars()[str(i) + 'ue'] = pd.read_csv(inpath + 'Avg/' + str(i) + 'ue.csv')

ms1 = ['pers', 'hisp', 'ed']
for j in ms1:
    vars()[str(j) + 'pctp2p' + str(per1)] = pd.read_csv(inpath + 'Avg/' + str(j) + 'pctp2p' + str(per1) + '.csv')
    vars()[str(j) + 'pctp2p' + str(per3)] = pd.read_csv(inpath + 'Avg/' + str(j) + 'pctp2p' + str(per3) + '.csv')
    vars()[str(j) + 'pctp2p' + str(per4)] = pd.read_csv(inpath + 'Avg/' + str(j) + 'pctp2p' + str(per4) + '.csv')
    vars()[str(j) + 'pctp2p' + str(per2)] = pd.read_csv(inpath + 'Avg/' + str(j) + 'pctp2p' + str(per2) + '.csv')
    vars()[str(j) + 'uep2p'] = pd.read_csv(inpath + 'Avg/' + str(j) + 'uep2p.csv')

vars()['dmapct' + str(per1)] = pd.read_csv(inpath + 'Avg/dmapct' + str(per1) + '.csv')
vars()['dmapct' + str(per3)] = pd.read_csv(inpath + 'Avg/dmapct' + str(per3) + '.csv')
vars()['dmapct' + str(per4)] = pd.read_csv(inpath + 'Avg/dmapct' + str(per4) + '.csv')
vars()['dmapct' + str(per2)] = pd.read_csv(inpath + 'Avg/dmapct' + str(per2) + '.csv')

vars()['dmapctp2p' + str(per1)] = pd.read_csv(inpath + 'Avg/dmapctp2p' + str(per1) + '.csv')
vars()['dmapctp2p' + str(per3)] = pd.read_csv(inpath + 'Avg/dmapctp2p' + str(per3) + '.csv')
vars()['dmapctp2p' + str(per4)] = pd.read_csv(inpath + 'Avg/dmapctp2p' + str(per4) + '.csv')
vars()['dmapctp2p' + str(per2)] = pd.read_csv(inpath + 'Avg/dmapctp2p' + str(per2) + '.csv')
dmaue = pd.read_csv(inpath + 'Avg/dmaue.csv')

exec(open('avg4lac.py').read())
# ----------------------------------------------------------------------------

# *********** Final Output File *********** 
hohinterue = vars()['hohinterue_' + str(period)].copy(deep=True)
ch16interue = vars()['ch16interue_' + str(period)].copy(deep=True)
hispinterue = vars()['hispinterue_' + str(period)].copy(deep=True)
edinterue = vars()['edinterue_' + str(period)].copy(deep=True)
reginterue = vars()['reginterue_' + str(period)].copy(deep=True)
hhszinterue = vars()['hhszinterue_' + str(period)].copy(deep=True)
persinteruep2p = vars()['persinteruep2p_' + str(period)].copy(deep=True)
hispinteruep2p = vars()['hispinteruep2p_' + str(period)].copy(deep=True)
edinteruep2p = vars()['edinteruep2p_' + str(period)].copy(deep=True)

dfs = [hohinterue, ch16interue, hispinterue, edinterue, reginterue, srtop1,
       reminterue, hhszinterue, persinteruep2p, hispinteruep2p, edinteruep2p,
       srtop2, reminteruep2p]
writer = pd.ExcelWriter(path + '\internet.' + str(period) + '.xlsx')
row = 0
for dataframe in dfs:
    dataframe.to_excel(writer, sheet_name='internet', startrow=row, startcol=0, index=False,header=False)
    row = row + len(dataframe.index) 
writer.save()


# ----------------------------------------------------------------------------
#                               Excel Automation
# ----------------------------------------------------------------------------

exec(open('Netview_excel.py').read())
