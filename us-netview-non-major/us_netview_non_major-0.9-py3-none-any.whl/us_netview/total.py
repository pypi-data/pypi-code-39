#import pandas as pd
#import numpy as np
#from openpyxl import load_workbook
#import xlwings as xw
#from datetime import datetime as dt
#import calendar
#from pathlib import Path 
#import os,sys

path = r"\\nadayisicifs03.dayisi03.enterprisenet.org\share3\SRData\UEData\Internet UEs\Any_Total_NOCR"
print('\n\n#################################################################')
print('\n Path for TotalUEsExpandedDemos Build input file: \n', path)
print('#################################################################')
#r"C:\Users\anal8003\Desktop\GOT\US netview UE non major\New folder\total\\"


#eperson2_path = r"\\nadayisicifs03.dayisi03.enterprisenet.org\share3\SRData\UEData\NielsenOnlineHomeUEs/"
#print("\nPath for ePerson2+ input file:\n ",eperson2_path)
#
#eperson2_path = eperson2_path  + curr_month1[:3]+curr_month1[5:]
#r"C:\Users\anal8003\Desktop\GOT\US netview UE non major\New folder (2)\"


#annual_update_path = r'\\nadayisicifs03.dayisi03.enterprisenet.org\share3\SRData\UEData\Internet UEs' \
#               '\Annual Update_{0}\Final Files Annual\Annual_Update_OnlineODM_Jan{0}_rpt.xlsx'.format(annual_year)
#C:\Users\anal8003\Desktop\GOT\AnnualUpdate


os.mkdir(path + "\\" + curr_process)

output_path = path + "\\" + curr_process
#output_path = r"C:\Users\anal8003\Desktop\GOT\US netview UE non major\New folder\total" + "\\" + curr_process

path = path + '\\' + prev_month[:3] + prev_month[5:]
print('\n\n#################################################################')
print("\nNew Directory created successfully \n" + output_path  )
print('#################################################################')
#----------------------------------------------------------------------------
#                     Total UEs Expanded Demos build 
#----------------------------------------------------------------------------


output_wb = xw.Book(path + "\TotalUEsExpandedDemos" + prev_month + "_Build.xlsx")
wks = output_wb.sheets[0]


#----------------------------------------------------------------------------
#                     Annual update file 
#----------------------------------------------------------------------------

workbook_ap = xw.Book(annual_wts_file_path)
wk1 = workbook_ap.sheets['Online Rpt_Pers']
TotHHPers = wk1.range('C8:C37').value
workbook_ap.close()

#----------------------------------------------------------------------------
#                     e_Persons2+ file
#----------------------------------------------------------------------------

workbook_eperson = xw.Book(eperson2_path + "\e_Persons2+_"+curr_process +".xlsx")
wk2 = workbook_eperson.sheets[0]
HomeInternet = wk2.range("C8:C37").value
workbook_eperson.close()

#----------------------------------------------------------------------------
#                     TotalInternetAccess Original file
#----------------------------------------------------------------------------

workbook_any = xw.Book(r"\\nadayisicifs03.dayisi03.enterprisenet.org\share3\SRData\UEData\Internet UEs\Any\Reports" \
                       "\TotalInternetAccess{0}.xlsx".format(curr_month1))

workbook_any.save(output_path + "\TotalInternetAccess" + curr_process + "_Original.xlsx")
wk_csv = workbook_any.sheets['UEs For Upload to Webstar']
df_csv = pd.DataFrame(wk_csv.range('A1:N12').options(header=None,index=False).value)
df_csv.to_csv(output_path +"/TotalInternetAccess" + curr_process + "_Original.csv",index=False, header =None)
workbook_any.close()

workbook_any = xw.Book(output_path + "\\TotalInternetAccess" + curr_process + "_Original.xlsx")
wk3 = workbook_any.sheets[0]
TotAccess =  wk3.range("E6:E17").value
workbook_any.close()

wks.range("K10").value = pd.DataFrame(TotAccess).values
wks.range("B10").value = pd.DataFrame(HomeInternet).values
wks.range("C10").value = pd.DataFrame(TotHHPers).values

wks = output_wb.sheets[3]
            
values_list = get_adjusted_values(wks.range("K1:K26").value)
print('\n\n#################################################################')
print("Sum of Adjusted value:",round(sum(values_list),2))
print('\n\n#################################################################')
      
wks.range("G1").value = pd.DataFrame(values_list).values

wks.range("H1:H26").value = '%s01%s'%(num_month,annual_year)

#wks.book.save(output_path + "\TotalUEsExpandedDemos" + curr_month1 + "_Build.xls")

wk_csv = output_wb.sheets[4]
df_csv = pd.DataFrame(wk_csv.range('A1:N26').options(header=None,index=False).value)

df_csv.to_csv(output_path + "\TotalInternetAccessUEs" + curr_process + "_Expanded.csv",index=False, header =None)
df_csv.to_excel(output_path + "\TotalInternetAccessUEs" + curr_process + "_Expanded.xlsx", \
                sheet_name ="UEs for Upload to Webstar",header=False, index=False)

SummaryBreaksExpand = output_wb.sheets[1]
SummaryBreaksExpand.range("A1").value = "Any Device / Any Location Internet UE - " + curr_month1[:3] + " " + curr_month1[3:]
#SummaryBreaksExpand.book.save(output_path + "\TotalUEsExpandedDemos" + curr_month1 + "_Build.xls")
SummaryBreaksCondensed = output_wb.sheets[2]
SummaryBreaksCondensed.range("A1").value = "Any Device / Any Location Internet UE - " + curr_month1[:3] + " " + curr_month1[3:]
#SummaryBreaksCondensed.book.save(output_path + "\TotalUEsExpandedDemos" + curr_month1 + "_Build.xls")

output_wb.save(output_path + "\TotalUEsExpandedDemos" + curr_month1 + "_Build.xlsx")


output_wb.close()
