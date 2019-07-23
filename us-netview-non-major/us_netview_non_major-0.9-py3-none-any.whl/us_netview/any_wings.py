#import xlwings as xw
#import pandas as pd
#from datetime import datetime as dt
#import os,sys
#import calendar
#import Lace
#import glob


path =r"\\nadayisicifs03.dayisi03.enterprisenet.org\share3\SRData\UEData\Internet UEs\Any\Processing"
print('\n\n#################################################################')
print("\nPath for TotalAccessUE input file:\n ",path)
print('#################################################################')
#path = input('\nPlease enter the Path for TotalAccessUE input file: \n')
list_of_files = glob.glob(r"\\nadayisicifs03.dayisi03.enterprisenet.org\share3\SRData\UEData\Internet UEs\Any\Processing\*.xlsx")
latest_file = max(list_of_files, key=os.path.getctime)

weights_file_path_odm = r'\\nadayisicifs03.dayisi03.enterprisenet.org\share3\SRData\UEData\Internet UEs' \
           '\Annual Update_{0}\Final Files Annual\ODM_AnnualControlUE_{0}.xlsx'.format(annual_year)

#input_file = input('\nPlease enter input filename: \n')
#path="C:\Users\anal8003\Desktop\Michelle Rebello\Netview Any\\"

#eperson2_path = r"\\nadayisicifs03.dayisi03.enterprisenet.org\share3\SRData\UEData\NielsenOnlineHomeUEs/"
#print("\nPath for ePerson2+ input file:\n ",eperson2_path)
#
#eperson2_path = eperson2_path  + curr_month1[:3]+curr_month1[5:]
#r"C:\Users\anal8003\Desktop\GOT\US netview UE non major\New folder (2)\"


#weights_file_path_annual = r'\\nadayisicifs03.dayisi03.enterprisenet.org\share3\SRData\UEData\Internet UEs' \
#           '\Annual Update_{0}\Final Files Annual\Annual_Update_OnlineODM_Jan{0}_rpt.xlsx'.format(annual_year)


#os.mkdir(path + "\\" + curr_process)

output_path = r"\\nadayisicifs03.dayisi03.enterprisenet.org\share3\SRData\UEData\Internet UEs\Any"
#output_path = r"C:\Users\anal8003\Desktop\GOT\US netview UE non major\New folder\any"
path = latest_file

wb = xw.Book(path)
try:    
    #----------------------------------------------------------------------------
    #                          SHEET 1 (PENETRATION -- ANY)
    #----------------------------------------------------------------------------
    
    sheet1 = wb.sheets[0]
    
    pen_any = round((p14['PERWT'].sum()/(p14['PERWT'].sum()+p15['PERWT'].sum()))*100, 2)
    endrange = sheet1.range('B1').end('down').row 
    quarter = file[-4:-2] + '-' + file[-2:]
    print('\n\n#################################################################')
    print("\nRunning Major Run\n")
    print('#################################################################')
    sheet1.range(endrange + 1,1).value = quarter
    sheet1.range(endrange + 1,2).value = pen_any
    sheet1.range(endrange + 1, 3).formula = '=ROUND(AVERAGE(B' + str(endrange -1)+ ':B' + str(endrange +1) + '),2)'
    
    print('\n\n#################################################################')
    print("\nRunning PENETRATION -- ANY\n")
    print('#################################################################')
    
    #----------------------------------------------------------------------------
    #                          SHEET 1 (PENETRATION -- HOME)
    #----------------------------------------------------------------------------
    
    #wb = xw.Book(path + "\\" + input_file)
    sheet2 = wb.sheets[1]
    
    pen_home = round((p16['PERWT'].sum()/(p16['PERWT'].sum()+p17['PERWT'].sum()))*100, 2)
    
    sheet2.range(endrange + 1,1).value = quarter
    sheet2.range(endrange + 1,2).value = pen_home
    sheet2.range(endrange + 1, 3).formula = '=ROUND(AVERAGE(B' + str(endrange -1)+ ':B' + str(endrange +1) + '),2)'
    print('\n\n#################################################################')
    print("\nRunning PENETRATION -- HOME\n")
    print('#################################################################')
    #----------------------------------------------------------------------------
    #                          SHEET 3 (4QTR AVG -- ANY)
    #----------------------------------------------------------------------------
    
    
    sheet3 = wb.sheets[2]

         
    weights_values_odm = pd.read_excel(weights_file_path_odm, sheet_name = 'ODM Table')
    weights_values_annual = pd.read_excel(annual_wts_file_path, sheet_name = 'Online_Rpt_P18+')
    age_gender_annual_weights = weights_values_odm[['Control UEs', 'Unnamed: 1']].dropna().iloc[:23]
    
    sheet3.range("I4").value = age_gender_annual_weights['Unnamed: 1'].iloc[0]
    
    inputs = sheet3.range("J5:J6").value
    col_target = age_gender_annual_weights['Unnamed: 1'].iloc[0]
    sheet3.range("K5:K6").value = pd.DataFrame(Lace.Lace.Lace1D(theTarget=col_target,arrayToLace=inputs,numDecimalPlaces=0)).values
    
    avg_any = count1
    
    avg_any['AGEUE'] = avg_any['AGEUE'].apply(lambda x: x.replace(' ',''))
    avg_any.reset_index(drop=True,inplace=True)
    avg_any['AGEUE'] = [avg_any['AGEUE'][i][:-1] for i in range(len(avg_any['AGEUE']))]
    
    value = []
    
    for cell1, cell2 in zip(sheet3.range('A5:A28').value, sheet3.range('B5:B28').value):
        #print(cell1, cell2)
        value.append([cell1, cell2]) 
    
    df_avg_any = pd.DataFrame(value) 
    df_avg_any['ANYFLAG'] = np.where(df_avg_any[1] == 'Yes', 1, 0)
    
    df_avg_any = df_avg_any.fillna(method = 'ffill')
    
    df_avg_any[0] = df_avg_any[0].str.upper()
    df_avg_any[0] = df_avg_any[0].apply(lambda x: x.replace(' ',''))
    df_avg_any.columns = ['AGEUE','Eligible','ANYFLAG']
    
    df_avg_any.reset_index(drop=True,inplace=True)
    
    avg_any_merge = df_avg_any.merge(avg_any, how = 'left', on = ['AGEUE', 'ANYFLAG'])
    avg_any_merge['Percent'].fillna(0,inplace=True)
    
    #moving data from Q2:Q4 to Q1:Q3
    
    sheet3.range('C5:C28').options(ndim = 2).value = sheet3.range('D5:D28').options(ndim = 2).value
    sheet3.range('D5:D28').options(ndim = 2).value = sheet3.range('E5:E28').options(ndim = 2).value
    sheet3.range('E5:E28').options(ndim = 2).value = sheet3.range('F5:F28').options(ndim = 2).value
    sheet3.range('F5:F28').options(index = False, header = False, ndim = 2).value = round(avg_any_merge[['Percent']], 4)
    
    print('\n\n#################################################################')
    print("\nRunning 4QTR AVG -- ANY\n")
    print('#################################################################')
    #----------------------------------------------------------------------------
    #                          SHEET 4 (4QTR AVG -- HOME)
    #----------------------------------------------------------------------------
    
    sheet4 = wb.sheets[3]
    
    sheet4.range("I4").value = age_gender_annual_weights['Unnamed: 1'].iloc[0]
    
    inputs = sheet4.range("J5:J6").value
    col_target = age_gender_annual_weights['Unnamed: 1'].iloc[0]
    sheet4.range("K5:K6").value = pd.DataFrame(Lace.Lace.Lace1D(theTarget=col_target,arrayToLace=inputs,numDecimalPlaces=0)).values
    
    avg_home = count2
    
    avg_home['AGEUE'] = avg_home['AGEUE'].apply(lambda x: x.replace(' ',''))
    avg_home.reset_index(drop=True,inplace=True)
    avg_home['AGEUE'] = [avg_home['AGEUE'][i][:-1] for i in range(len(avg_home['AGEUE']))]
    
    
    df_avg_home = df_avg_any
    df_avg_home.rename(columns={'ANYFLAG': 'HOMEFLAG'}, inplace = True)
    avg_home_merge = df_avg_home.merge(count2, how = 'left', on = ['AGEUE', 'HOMEFLAG'])
    avg_home_merge['Percent'].fillna(0,inplace=True)
    
    #moving data from Q2:Q4 to Q1:Q3
    
    sheet4.range('C5:C28').options(ndim = 2).value = sheet4.range('D5:D28').options(ndim = 2).value
    sheet4.range('D5:D28').options(ndim = 2).value = sheet4.range('E5:E28').options(ndim = 2).value
    sheet4.range('E5:E28').options(ndim = 2).value = sheet4.range('F5:F28').options(ndim = 2).value
    sheet4.range('F5:F28').options(index=False, header = False, ndim = 2).value = round(avg_home_merge['Percent'], 4)
    
    print('\n\n#################################################################')
    print("\nRunning 4QTR AVG -- HOME\n")
    print('#################################################################')
    #----------------------------------------------------------------------------
    #                          SHEET 5 (AGESEX -- ANY)
    #----------------------------------------------------------------------------
    
    sheet5 = wb.sheets[4]
    
    
    sheet5.range('E32').value = pd.DataFrame([age_gender_annual_weights.iloc[s:e]['Unnamed: 1'].sum() \
    for s,e in [(1,3), (3,5), (5,7), (7,9), (9,11), (11,12), \
                (12,14), (14,16), (16,18), (18,20), (20,22), (22,23)]]).values
    
       
    
    agesex_any = sheet5.range('B32:C43').options(index=False, header = False).value
    agesex_any = pd.DataFrame(agesex_any)
    agesex_any.columns = ['No', 'Yes']
    
    row_target_any = sheet5.range('E32:E43').options(index=False, header=False).value
    
    col_target_any = sheet5.range('B44:C44').options(index=False, header=False).value
    
    lace_values_any = Lace.Lace.Lace2D(25,col_target_any,row_target_any,agesex_any.values)
    
    sheet5.range('B48:C59').options(index=False, header=False).value = lace_values_any
    
    print('\n\n#################################################################')
    print("\nAGESEX -- ANY\n")        
    print('#################################################################')
    #----------------------------------------------------------------------------
    #                          SHEET 6 (AGESEX -- HOME)
    #----------------------------------------------------------------------------
    
    
    sheet6 = wb.sheets[5] 
    
    sheet6.range('E32').value = pd.DataFrame([age_gender_annual_weights.iloc[s:e]['Unnamed: 1'].sum() \
    for s,e in [(1,3), (3,5), (5,7), (7,9), (9,11), (11,12), \
                (12,14), (14,16), (16,18), (18,20), (20,22), (22,23)]]).values
    
        
    agesex_home = sheet6.range('B32:C43').options(index=False, header = False).value
    agesex_home = pd.DataFrame(agesex_home)
    agesex_home.columns = ['No', 'Yes']
    
    row_target_home = sheet6.range('E32:E43').options(index=False, header=False).value
    
    col_target_home = sheet6.range('B45:C45').options(index=False, header=False).value
    
    lace_values_home = Lace.Lace.Lace2D(25,col_target_home,row_target_home,agesex_home.values)
    
    sheet6.range('B49:C60').options(index=False, header=False).value = lace_values_home
    print('\n\n#################################################################')
    print("\nRunning AGESEX -- HOME\n")
    print('#################################################################')
except:
    print('\n\n#################################################################')
    print("\nRunning Non Major Run\n")
    print('#################################################################')
finally:

    #----------------------------------------------------------------------------
    #                          SHEET 7 (UNIVERSAL COMPUTATION)
    #----------------------------------------------------------------------------
    
    wb_ep = xw.Book(eperson2_path + "/e_Persons2+_"+curr_process+".xlsx")
    sheet = wb_ep.sheets[0]
    
    sheet7 = wb.sheets[6]
    
    sheet7.range('L26:L55').options(index=False, header=False).value = sheet.range('C8:C37').options(ndim = 2).value
    
    unv_comp = pd.DataFrame(sheet7.range('C46:D57').options(index=False, header = False).value)
    unv_comp['Target'] = sheet7.range('F46:F57').options(index=False, header = False).value
    unv_comp.columns = ['Out_of_Home_Only', 'No_Internet','Target']
    
    lace1D_values = []
    for i in range(len(unv_comp.values)):
    #    print(unv_comp.Target[i])
    #    print(list(unv_comp.iloc[i,:2].values))
        lace1D_values.append(Lace.Lace.Lace1D(theTarget=unv_comp.Target[i],arrayToLace=list(unv_comp.iloc[i,:2].values),numDecimalPlaces=0))
        
    sheet7.range('C60:D71').options(index=False, header=False).value = lace1D_values
    print('\n\n#################################################################')
    print("\nRunning UNIVERSAL COMPUTATION\n")
    print('#################################################################')
    
    
    
    
    
    #----------------------------------------------------------------------------
    #                          Total Internet Access
    #----------------------------------------------------------------------------
    
    sheet8 = wb.sheets[7]
    
    sheet8.range("A1").value = "Any Device / Any Location Internet UE - " + curr_month1[:3] + " " + curr_month1[3:]
    quarter = str(pd.Period(datetime.date.today(), freq='M').asfreq('Q-DEC'))[:5] + \
        str(int(str(pd.Period(datetime.date.today(), freq='M').asfreq('Q-DEC'))[5:]) + 1)
        
    sheet8.range("A2").value ="Based on Phoning results from "+ quarter+" NetView Enumeration and "+ \
                                    curr_month1+" NPM-Based Persons 18+ Internet UE"
    
    wb1 = xw.Book(r"\\nadayisicifs03.dayisi03.enterprisenet.org\share3\SRData\UEData\Internet UEs\Any\Reports\TotalInternetAccess" + prev_month + ".xlsx" )
    sheet9 = wb1.sheets[0]
    
    sheet9.range("A1").value = "Any Device / Any Location Internet UE - " + curr_month1[:3] + " " + curr_month1[3:]

    sheet9.range("A2").value ="Based on Phoning results from "+ quarter+" NetView Enumeration and "+ \
                                    curr_month1+" NPM-Based Persons 18+ Internet UE"										

    sheet9.range('B6:K21').options(index=False, header=False).value = sheet8.range('B6:K21').options(ndim = 2).value
    
    
    def get_adjusted_values(orig_val):
       check_list = [round(x,4) for x in orig_val]
       values_list = [round(x,2) for x in check_list]
       final_check_list_1 = []
       final_check_list_2 = []
       if round(sum(values_list),2) != 100: 
           for i,val in enumerate(check_list):
               try:
                   if int(str(val)[-2:])>50:
                       final_check_list_1.append((i,int(str(val)[-2:])))
                   elif int(str(val)[-2:])<50:
                       final_check_list_2.append((i,int(str(val)[-2:]))) 
               except: pass
       if round(sum(values_list),2) > 100:
           sort_final_1 = sorted(final_check_list_1, key=lambda x: x[1])
           for i in sort_final_1:
               if round(sum(values_list),2) != 100: 
                   values_list[i[0]] = values_list[i[0]] - 0.01
       else:
           sort_final_2 = sorted(final_check_list_2, key=lambda x: x[1], reverse = True)
           #print('Sort final 2:',sort_final_2)
           for i in sort_final_2:
               if round(sum(values_list),2)!= 100: 
                   #print('Old Val:', values_list[i[0]])
                   values_list[i[0]] = values_list[i[0]] + 0.01
                   #print('New Val:', values_list[i[0]])
                   #print('Final Sum: ',round(sum(values_list),2))
                   
       values_list = [round(x,2) for x in values_list]
       #print('Final Value list: ',values_list)
       return values_list
    
    print('\n\n#################################################################')
    print("\nRunning Total Internet Access\n")
    print('#################################################################')
    sheet10 = wb1.sheets[1]
    
    org_val = sheet10.range('K1:K12').options(index=False, header=False).value
    
    fnl_val = pd.DataFrame(get_adjusted_values(org_val))
    
    sheet10.range('G1:G12').options(index = False, header = False).value = fnl_val
    sheet10.range('H1:H12').value = '%s01%s'%(num_month,annual_year)
    
    wb.save(output_path + "/Processing/TotalAccessUEQ418-Q219-" + curr_process[:3] + ".xlsx")
    wb1.save(output_path + "/Reports/TotalInternetAccess" + curr_month1 + ".xlsx" )
    wb1.close()
    wb.close()
    wb_ep.close()
    
