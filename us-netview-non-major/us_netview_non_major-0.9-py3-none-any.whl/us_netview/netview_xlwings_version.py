#  # Automation Assumptions:
#  
# 1- This Python Automation script is used to generate the Home UE excel sheets required for 
#    US Netview Non-Major run.It uses xlwings library to create required excel files
#  
# 2- Required Inputs
#    It required following input files:
#    (1)internet.mmmyy
#    (2)Annual_Update_OnlineODM_mmmyyyy_rpt.xlsx
#     
# 3- Required Excel Templates (All templates are provided with script)
#    It required following templates:
#    (1)HomeInternetUE_Calcs.xlsx
#    (2)e_NNR_HomeUEs.xlsx
#    (3)e_Persons2+.xlsx
#    (4)Procedures for Computing Spanish Language UEs.xlsx
#
# 4- Outputs (Saved at output path given by user)
#    (1)HomeInternetUE_Calcs_mmmyy.xlsx
#    (2)e_NNR_HomeUEs_mmmyy.xlsx
#    (3)e_Persons2+_mmmyy.xlsx
#    (4)Procedures for Computing Spanish Language UEs_mmmyy.xlsx
#    (5)HHUEs_yymm01.csv
#    (6)PersonsUEs_yymm01.csv

#import pandas as pd
#from datetime import datetime as dt
#import sys
#import re
#import time
#import numpy as np
#import xlwings as xw
#import os
#import Lace
#import calendar

# Wrting data to Excel Workbook
#full_year = dt.now().year
last_2_digit_year = str(annual_year)[2:]
month = curr_month1[:3]
num_month = "{:02d}".format((dt.now().month+1))

output_path = input('\nPlease enter the path for output:\n')
#\\nadayisicifs03.dayisi03.enterprisenet.org\share3\SRData\UEData\NielsenOnlineHomeUEs
os.mkdir(output_path + "\\" + curr_process)
output_path =  output_path + "\\" + curr_process

# DMA Name correction in internet file
# Below function takes short dma_name as input and
# returns the correct dma_name as output
def dma_name_correction(dma_name):
    print(dma_name)
    if dma_name.startswith('Boston'):
        dma_name = 'Boston'
    elif dma_name == 'Cleveland-Akron (Canton)':
        dma_name = 'Cleveland'
    elif dma_name == 'Columbus, OH':
        dma_name = 'Columbus'    
    elif dma_name == 'Dallas-Ft. Worth':
        dma_name = 'Dallas'
    elif dma_name == 'Hartford & New Haven':
        dma_name = 'Hartford/New Haven'
    elif dma_name == 'Miami-Ft. Lauderdale':
        dma_name = 'Miami'
    elif dma_name == 'Minneapolis-St. Paul':
        dma_name = 'Minneapolis'
    elif dma_name == 'Orlando-Daytona Bch-Melbrn':
        dma_name = 'Orlando'
    elif dma_name == 'Phoenix (Prescott)':
        dma_name = 'Phoenix'
    elif dma_name == 'Portland, OR':
        dma_name = 'Portland'
    elif dma_name == 'Raleigh-Durham (Fayetvlle)':
        dma_name = 'Raleigh-Durham, NC.'
    elif dma_name == 'Sacramnto-Stkton-Modesto':
        dma_name = 'Sacramento'
    elif dma_name == 'San Francisco-Oak-San Jose':
        dma_name = 'San Francisco'
    elif dma_name == 'Seattle-Tacoma':
        dma_name = 'Seattle'
    elif dma_name == 'Tampa-St. Pete (Sarasota)':
        dma_name = 'Tampa'
    elif dma_name == 'Washington, DC (Hagrstwn)':
        dma_name = 'Washington DC'
    elif dma_name == 'Reminder US':
        dma_name = 'Remainder U.S.'
    else:
        dma_name = dma_name
    return dma_name


def check_path(path):
    decision = False
    if os.path.exists(path):
        print('Valid Path....\n')
        decision = True
    else:
        print('Invalid Path...\n')
    return decision

def check_file(filepath_name):
    decision = False
    if os.path.isfile(filepath_name):
        print('Valid File...\n')
        decision = True
    else:
        print('Invalid File Name...\n')
    return decision


#############################################
# Reading Section Start
#############################################


# Reading internet input file
#while True:
while True:
    try:
        internet_file_path = input('\nPlease enter the path for internet input file: \n')
        if check_path(internet_file_path):
            break
        else:
            continue
    except:
        print('Invalid internet file path, Please enter a valid path: \n')
        continue
        
while True:
    try:
        internet_file_name = input('Please enter the internet file name: (For Ex: internet.MMMYY)\n')
        if check_file(internet_file_path + '//' + internet_file_name):
            try:
#                lines = []
#                with open(internet_file_path + '//' + internet_file_name,'r') as f:
#                    for line in f:
#                        lines.append(re.split(r'\s{2,}', line))
#                internet_month_df = pd.DataFrame(lines)
                internet_month_df = pd.read_excel(internet_file_path + '//' + internet_file_name,header=None,names=['index',0,1])
#                internet_month_df[0] = internet_month_df[0].str.replace('"','').str.strip()
#                internet_month_df[3] = ''
#                internet_month_df = internet_month_df[[0,3,1,2]]
#                internet_month_df[1] = internet_month_df[1].astype(int)
#                internet_month_df[2] = internet_month_df[2].astype(int)
                break
            except:
                print('Exception Internet file not found, Please check again...\n')
                continue
        else:
            print('Internet file not found, Please check again...\n')
            continue
    except:
        print('Invalid internet file name, Please enter a valid file name:\n')
        continue


# Reading Annual weights

while True:
    try:
        #annual_wts_file_path = input('\nPlease enter the path for Annual weights input file: \n')
        annual_wts_file_path = r'\\nadayisicifs03.dayisi03.enterprisenet.org\share3\SRData\UEData\Internet UEs' \
                           '\Annual Update_{0}\Final Files Annual\Annual_Update_OnlineODM_Jan{0}_rpt.xlsx'.format(annual_year)
        break
#        if check_path(annual_wts_file_path):
#            break
#        else:
#            continue
    except:
        print('Invalid annual weights path, Please enter a valid path:\n')
        continue

        
while True:
    try:
        if month == 'Sep':
            print('\nHello User, It September , Please use new Annual Update weights...')
#            annual_wts_file_name = input('\nPlease enter the Annual weights file name: (For Ex: Annual_Update_OnlineODM_MMMYYYY_rpt.xlsx) \n')
            annual_wts_file_path = r'\\nadayisicifs03.dayisi03.enterprisenet.org\share3\SRData\UEData\Internet UEs' \
                           '\Annual Update_{0}\Final Files Annual\Annual_Update_OnlineODM_Jan{0}_rpt.xlsx'.format(annual_year)
            #annual_wts_file_name = 'Annual_Update_OnlineODM_Jan{0}_rpt.xlsx'.format(year)
            #if check_file(annual_wts_file_path + '\\' + annual_wts_file_name):
            try:
                '''
                if dt.now().month >= 9:
                    weights_file_year = str(dt.now().year + 1)
                else:
                    weights_file_year = str(dt.now().year)
                '''
                #weights_file_path = annual_wts_file_path + '//' + annual_wts_file_name
                hh_weights_df = pd.read_excel(annual_wts_file_path, 
                                              sheet_name = 'Online Rpt_HHs',
                                              usecols=[0,2],header=None)
                
                per_weights_df = pd.read_excel(annual_wts_file_path, 
                                              sheet_name = 'Online Rpt_Pers',
                                              usecols=[0,2],header=None)
            
                # Dropping junk rows
                hh_weights_df.drop([0,1,2,3,4,5],inplace=True,axis=0)
                per_weights_df.drop([0,1,2,3,4,5,6],inplace=True,axis=0)
                
                # Index Reset for proper indexing
                per_weights_df.reset_index(drop=True,inplace=True)
                
                # Original person weights dataframe
                per_weights_orig_df = per_weights_df.copy(deep=True)
                print('\nHello User, Please make sure your are using the correct weights...')
                time.sleep(3)
                print('\nPlease find below the weight values for HH and Person: \n')
                
                print('HH Weigths :\n',hh_weights_df[:6].to_string(index=False))
                print('\nPerson Weigths :\n',per_weights_df[:6].to_string(index=False))
                break
            except Exception as e:
                print('Exception caught',str(e))
                print('Annual_Update_OnlineODM_%s'%month+ str(weights_file_year) +'.xlsx does not exists or incorrect file path...')
                sys.exit()
                
            #else:
            #print('Annual wts file not found, Please check again...\n')
            #continue            
        else:
            annual_wts_file_path = r'\\nadayisicifs03.dayisi03.enterprisenet.org\share3\SRData\UEData\Internet UEs' \
                           '\Annual Update_{0}\Final Files Annual\Annual_Update_OnlineODM_Jan{0}_rpt.xlsx'.format(annual_year)
#            annual_wts_file_name = input('\nPlease enter the Annual weights file name: (For Ex: Annual_Update_OnlineODM_MMMYYYY_rpt.xlsx) \n')
            #annual_wts_file_name = 'Annual_Update_OnlineODM_Jan{0}_rpt.xlsx'.format(year)
            #if check_file(annual_wts_file_path + '\\' + annual_wts_file_name):
            try:
                '''
                if dt.now().month >= 7:
                    weights_file_year = str(dt.now().year + 1)
                else:
                    weights_file_year = str(dt.now().year)
                    '''
                #weights_file_path = annual_wts_file_path + '\\' + annual_wts_file_name
                hh_weights_df = pd.read_excel(annual_wts_file_path, 
                                              sheet_name = 'Online Rpt_HHs',
                                              usecols=[0,2],header=None)
                
                per_weights_df = pd.read_excel(annual_wts_file_path, 
                                              sheet_name = 'Online Rpt_Pers',
                                              usecols=[0,2],header=None)
            
                # Dropping junk rows
                hh_weights_df.drop([0,1,2,3,4,5],inplace=True,axis=0)
                per_weights_df.drop([0,1,2,3,4,5,6],inplace=True,axis=0)
                
                # Index Reset for proper indexing
                per_weights_df.reset_index(drop=True,inplace=True)
                
                # Original person weights dataframe
                per_weights_orig_df = per_weights_df.copy(deep=True)
                print('\nHello User, Please make sure your are using the correct weights...')
                time.sleep(3)
                print('\nPlease find below the weight values for HH and Person: \n')
                
                print('HH Weigths :\n',hh_weights_df[:6].to_string(index=False))
                print('\nPerson Weigths :\n',per_weights_df[:6].to_string(index=False))
                break
            except Exception as e:
                print('Exception caught',str(e))
                print('Annual_Update_OnlineODM_%s'%month+ str(weights_file_year) +'.xlsx does not exists or incorrect file path...')
                sys.exit()
                
            #else:
            #print('Annual wts file not found, Please check again...\n')
            #continue
    except:
        print('Invalid Annual weights file name, Please enter a valid file name:\n')


# Use Input decision
user_input = input('\nAbove weights are correct ?\nPlease Validate(Yes/No) :\n')

if user_input == 'Yes' or  user_input == 'yes' or user_input == 'YES':
    
    #########################################################
    # HomeInternetUE_Calcs_mmmyy.xlsx Workbook Section Starts
    #########################################################
    wb = xw.Book(r'Templates/HomeInternetUE_Calcs.xlsx')
    
    # Updating Input sheet
    input_sheet  = wb.sheets['Input']
    input_sheet.range('A1').options(index=False,header=None).value = internet_month_df
    
    total_male_category = internet_month_df[94:124][0].sum()
    total_female_category = internet_month_df[94:124][1].sum()
    total_gender = total_male_category + total_female_category
    #############################################
    # Updating Rpt_HHs sheet Section Start
    #############################################
    rpt_HH_sheet  = wb.sheets['Rpt_HHs']
    rpt_HH_sheet.range('A1').value = 'Nielsen/NetRatings TOTAL HOUSEHOLDS Internet Universe Estimates (000) Used for %s %s'%(month, annual_year)
    hh_weights_df.reset_index(drop=True,inplace=True)
    
    hh_weights_df[0]  = hh_weights_df[0].str.strip()
    
    # Adding Buffalo value becaue of wrong sort order in Annual weights
#    buffalo_val = hh_weights_df[hh_weights_df[0] == 'Buffalo'][2].values[0]
    buffalo_val = hh_weights_df[hh_weights_df[0] == 'Buffalo'][1].values[0]
#    bufallo_df = pd.DataFrame({0: 'Buffalo', 2 : buffalo_val }, index=[64])
    bufallo_df = pd.DataFrame({0: 'Buffalo', 1 : buffalo_val }, index=[64])
    hh_weights_df = pd.concat([hh_weights_df.loc[:63], bufallo_df, hh_weights_df.loc[64:]]).reset_index(drop=True)
    hh_weights_df.drop(hh_weights_df[(hh_weights_df[0] == 'Buffalo')].index[-1],inplace=True)
    
    # Adding Jacksonville value becaue of wrong sort order in Annual weights
    #jacksonville_val = hh_weights_df[hh_weights_df[0] == 'Jacksonville'][2].values[0]
    jacksonville_val = hh_weights_df[hh_weights_df[0] == 'Jacksonville'][1].values[0]
#    jacksonville_df = pd.DataFrame({0: 'Jacksonville', 2 : jacksonville_val }, index=[80])
    jacksonville_df = pd.DataFrame({0: 'Jacksonville', 1 : jacksonville_val }, index=[80])
    hh_weights_df = pd.concat([hh_weights_df.loc[:79], jacksonville_df, hh_weights_df.loc[80:]]).reset_index(drop=True)
    hh_weights_df.drop(hh_weights_df[(hh_weights_df[0] == 'Jacksonville')].index[-1],inplace=True)
    
    # Adding Providence-New Bedford value becaue of wrong sort order in Annual weights
    #providence_val = hh_weights_df[hh_weights_df[0] == 'Providence-New Bedford'][2].values[0]
    providence_val = hh_weights_df[hh_weights_df[0] == 'Providence-New Bedford'][1].values[0]
#    providence_df = pd.DataFrame({0: 'Providence-New Bedford', 2 : providence_val }, index=[100])
    providence_df = pd.DataFrame({0: 'Providence-New Bedford', 1 : providence_val }, index=[100])
    hh_weights_df = pd.concat([hh_weights_df.loc[:99], providence_df, hh_weights_df.loc[100:]]).reset_index(drop=True)
    hh_weights_df.drop(hh_weights_df[(hh_weights_df[0] == 'Providence-New Bedford')].index[-1],inplace=True)
#    rpt_HH_sheet.range('M7').options(index=False,header=None).value = hh_weights_df[2]
    rpt_HH_sheet.range('M7').options(index=False,header=None).value = hh_weights_df[1]
#    e_NNR_HomeUEs_input = rpt_HH_sheet.range('A1:N135').options(index=False,header=None).value
    e_NNR_HomeUEs_input = rpt_HH_sheet.range('A1:M135').options(index=False,header=None).value
    #############################################
    # Updating Rpt_HHs sheet Section Ends
    #############################################
    
    #############################################
    # Updating Rpt_Pers sheet Section Start
    #############################################
    rpt_Per_sheet  = wb.sheets['Rpt_Pers']
    rpt_Per_sheet.range('A1').value = 'Nielsen/NetRatings Persons 2+ in TOTAL HOMES Internet Panel Universe Estimates (000) for %s %s'%(month,annual_year)
    
    per_weights_df[0]  = per_weights_df[0].str.strip()
    
    # Dropping some un-necessary Spanish/Non-Spanish Values
    per_weights_df.drop(per_weights_df.index[range(39,52)],axis=0,inplace=True)
    per_weights_df.reset_index(drop=True,inplace=True)
    
    # Adding Person Buffalo value becaue of wrong sort order in Annual weights
    #per_buffalo_val = per_weights_df[per_weights_df[0] == 'Buffalo'][2].values[0]
    per_buffalo_val = per_weights_df[per_weights_df[0] == 'Buffalo'][1].values[0]
#    per_bufallo_df = pd.DataFrame({0: 'Buffalo', 2 : per_buffalo_val }, index=[57])
    per_bufallo_df = pd.DataFrame({0: 'Buffalo', 1 : per_buffalo_val }, index=[57])
    per_weights_df = pd.concat([per_weights_df.loc[:56], per_bufallo_df, per_weights_df.loc[57:]]).reset_index(drop=True)
    per_weights_df.drop(per_weights_df[(per_weights_df[0] == 'Buffalo')].index[-1],inplace=True)
    
    # Adding Person Jacksonville value becaue of wrong sort order in Annual weights
    #per_jacksonville_val = per_weights_df[per_weights_df[0] == 'Jacksonville'][2].values[0]
    per_jacksonville_val = per_weights_df[per_weights_df[0] == 'Jacksonville'][1].values[0]
#    per_jacksonville_df = pd.DataFrame({0: 'Jacksonville', 2 : per_jacksonville_val }, index=[73])
    per_jacksonville_df = pd.DataFrame({0: 'Jacksonville', 1 : per_jacksonville_val }, index=[73])
    per_weights_df = pd.concat([per_weights_df.loc[:72], per_jacksonville_df, per_weights_df.loc[73:]]).reset_index(drop=True)
    per_weights_df.drop(per_weights_df[(per_weights_df[0] == 'Jacksonville')].index[-1],inplace=True)
    
    # Adding Person Providence-New Bedford value becaue of wrong sort order in Annual weights
    #per_providence_val = per_weights_df[per_weights_df[0] == 'Providence-New Bedford'][2].values[0]
    per_providence_val = per_weights_df[per_weights_df[0] == 'Providence-New Bedford'][1].values[0]
#    per_providence_df = pd.DataFrame({0: 'Providence-New Bedford', 2 : per_providence_val }, index=[93])
    per_providence_df = pd.DataFrame({0: 'Providence-New Bedford', 1 : per_providence_val }, index=[93])
    per_weights_df = pd.concat([per_weights_df.loc[:92], per_providence_df, per_weights_df.loc[93:]]).reset_index(drop=True)
    per_weights_df.drop(per_weights_df[(per_weights_df[0] == 'Providence-New Bedford')].index[-1],inplace=True)
#    rpt_Per_sheet.range('M8').options(index=False,header=None).value = per_weights_df[2]
    rpt_Per_sheet.range('M8').options(index=False,header=None).value = per_weights_df[1]
    rpt_Per_sheet['K120'].value = '=IF(AND(K39,K46,K55,K117=%s),"OK","BAD")'%total_gender
    e_Per_two_plus_input = rpt_Per_sheet.range('A1:M118').options(index=False,header=None).value
    rpt_Per_sheet.range('M47').value = ''
    
    #############################################
    # Updating Rpt_Pers sheet Section Ends
    #############################################
    
    wb.save(output_path + '//' + 'HomeInternetUE_Calcs_%s%s.xlsx'%(month,last_2_digit_year))
    wb.close()
    
    #######################################################
    # HomeInternetUE_Calcs_mmmyy.xlsx Workbook Section Ends
    #######################################################
    
    
    ##########################################################################################
    
    
    
    
    #########################################################
    # e_NNR_HomeUEs_mmmyy.xlsx Workbook Section Starts
    #########################################################
    wb_e_NNR = xw.Book(r'Templates/e_NNR_HomeUEs.xlsx')
    
    # Reading data from "Reporting UEs" sheet
    rep_UE_hh_sht = wb_e_NNR.sheets['Reporting UEs']
    
    # Updating new values in "Reporting UEs" sheet
    rep_UE_hh_sht.range('A1').options(index=False,header=None).value = e_NNR_HomeUEs_input
    
    # Reading data from "RAW UEs for Upload_NNR" sheet
    raw_UE_upload_sht = wb_e_NNR.sheets['RAW UEs for Upload_NNR']
    
    # Date(MMDDYYYY) in column H
    raw_UE_upload_sht.range('H1:H91').value = '%s01%s'%(num_month,annual_year)
    # Creating dataframe for "RAW UEs for Upload_NNR" sheet
    raw_UE_upload_df = raw_UE_upload_sht.range('A1:J91').options(pd.DataFrame,header=0,index=False).value
       
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
    
    # Getting HH Categories values
    raw_UE_upload_df[2] = raw_UE_upload_df[2].str.strip()
    
    print('\n#################################################################')
    print('Validating HH Adjusted sum for "RAW UEs for Upload_NNR" sheet in e_NNR_HomeUEs_mmmyy.xlsx')
    print('#################################################################\n')
    hh_age_of_hoh_val = list(raw_UE_upload_df[raw_UE_upload_df[2] == 'AgeHOH'][6])
    hh_age_of_hoh_adj_val = get_adjusted_values(hh_age_of_hoh_val)
    hh_age_of_hoh_adj_sum = round(sum(hh_age_of_hoh_adj_val),2)
    print('\nHH Age of HOH Adjusted Sum: ',hh_age_of_hoh_adj_sum)
    assert(hh_age_of_hoh_adj_sum == 100),'HH Age of HOH adjusted sum for RAW UEs for Upload_NNR sheet failed, exiting now...'
    raw_UE_upload_sht.range('I1').options(transpose=True).value = hh_age_of_hoh_adj_val
    
    hh_child_val = list(raw_UE_upload_df[raw_UE_upload_df[2] == 'Child'][6])
    hh_child_adj_val = get_adjusted_values(hh_child_val)
    hh_child_adj_sum = round(sum(hh_child_adj_val),2)
    print('HH Child Adjusted Sum: ',hh_child_adj_sum)
    assert(hh_child_adj_sum == 100),'HH Child adjusted sum for RAW UEs for Upload_NNR sheet failed, exiting now...'
    raw_UE_upload_sht.range('I7').options(transpose=True).value = hh_child_adj_val
    
    hh_hhsize_val = list(raw_UE_upload_df[raw_UE_upload_df[2] == 'HHsize'][6])
    hh_hhsize_adj_val = get_adjusted_values(hh_hhsize_val)
    hh_hhsize_adj_sum = round(sum(hh_hhsize_adj_val),2)
    print('HH Size Adjusted Sum: ',hh_hhsize_adj_sum)
    assert(hh_hhsize_adj_sum == 100),'HH Size adjusted sum for RAW UEs for Upload_NNR sheet failed, exiting now...'
    raw_UE_upload_sht.range('I23').options(transpose=True).value = hh_hhsize_adj_val

    hh_edu_of_hoh_val = list(raw_UE_upload_df[raw_UE_upload_df[2] == 'EducationHOH'][6])
    hh_edu_of_hoh_adj_val = get_adjusted_values(hh_edu_of_hoh_val)
    hh_edu_of_hoh_adj_sum = round(sum(hh_edu_of_hoh_adj_val),2)
    print('HH EducationofHOH Adjusted Sum: ',hh_edu_of_hoh_adj_sum)
    assert(hh_edu_of_hoh_adj_sum == 100),'HH EducofHOH adjusted sum for RAW UEs for Upload_NNR sheet failed, exiting now...'
    raw_UE_upload_sht.range('I28').options(transpose=True).value = hh_edu_of_hoh_adj_val
    
    hh_hispanic_hoh_val = list(raw_UE_upload_df[raw_UE_upload_df[2] == 'HispanicHOH'][6])
    hh_hispanic_hoh_adj_val = get_adjusted_values(hh_hispanic_hoh_val)
    hh_hispanic_hoh_adj_sum = round(sum(hh_hispanic_hoh_adj_val),2)
    print('HH Hispanic Adjusted Sum: ',hh_hispanic_hoh_adj_sum)
    assert(hh_hispanic_hoh_adj_sum == 100),'HH Hispanic adjusted sum for RAW UEs for Upload_NNR sheet failed, exiting now...'
    raw_UE_upload_sht.range('I32').options(transpose=True).value = hh_hispanic_hoh_adj_val
    
    hh_state_val = list(raw_UE_upload_df[raw_UE_upload_df[2] == 'State'][6])
    hh_state_adj_val = get_adjusted_values(hh_state_val)
    hh_state_adj_sum = round(sum(hh_state_adj_val),2)
    print('HH State Adjusted Sum: ',hh_state_adj_sum)
    assert(hh_state_adj_sum == 100),'HH State adjusted sum for RAW UEs for Upload_NNR sheet failed, exiting now...'
    raw_UE_upload_sht.range('I34').options(transpose=True).value = hh_state_adj_val
    
    #hh_total = raw_UE_upload_df[raw_UE_upload_df[2] == 'Total'][6].values[0]
    
    
    
    # Reading data from HH FTP sheet and saving it to HHUEs_yymmdd.csv file
    ftp_sht = wb_e_NNR.sheets['FTP']
    ftp_df = ftp_sht.range('A1:H91').options(pd.DataFrame,header=0,index=False).value
    ftp_df.to_csv(output_path + '//' + 'HHUEs_%s%s01.csv'%(last_2_digit_year,num_month),index=False,header=None)
    
    wb_e_NNR.save(output_path + '//' + 'e_NNR_HomeUEs_%s%s.xlsx'%(month,last_2_digit_year))
    wb_e_NNR.close()
    print('\n#################################################################')
    print('HH Validation completed successfully!!!')
    print('#################################################################\n')
    #######################################################
    # e_NNR_HomeUEs_mmmyy.xlsx Workbook Section Ends
    #######################################################
    
    ##########################################################################################
    
    

    #########################################################
    # e_Persons2+_mmmyy.xlsx Workbook Section Starts
    #########################################################
    wb_e_Per = xw.Book(r'Templates/e_Persons2+.xlsx')
    
    # Reading data from "Monthly Universe Estimates" sheet
    rep_UE_per_sht = wb_e_Per.sheets['Monthly Universe Estimates']
    
    # Updating new values in "Monthly Universe Estimates" sheet
    rep_UE_per_sht.range('A1:M117').options(index=False,header=None).value = e_Per_two_plus_input


    ##########################################################
    ##########################################################
    # Calling SLDUE.py for Hispanic/Non-Hisapanic calculation
    ##########################################################
    ##########################################################
    print('\nStarting work on SLD UE...')
    exec(open('SLDUE.py').read())
    print('SLD UEs completed Successfully!!!\n ')
    
    # Updating values from SLD UE for Hispanic identity of HH
    rep_UE_per_sht.range('A43:L46').options(index=False,header=None).value = ethnic_df
    
    # Specific data for Person 2+ Hispanic and Non-Hispanic
    # We are doing this because of bad/weird format in Annual Update file
    per_weights_orig_df[0] = per_weights_orig_df[0].str.strip()
#    annual_weights_hispanic_val = per_weights_orig_df[per_weights_orig_df[0] == 'Hispanic/Latino/Spanish'][2].values[0]
#    annual_weights_non_hisp_val = per_weights_orig_df[per_weights_orig_df[0] == 'Not Hispanic/Latino/Spanish'][2].values[0]
    annual_weights_hispanic_val = per_weights_orig_df[per_weights_orig_df[0] == 'Hispanic/Latino/Spanish'][1].values[0]
    annual_weights_non_hisp_val = per_weights_orig_df[per_weights_orig_df[0] == 'Not Hispanic/Latino/Spanish'][1].values[0]
    total_eth_sum = annual_weights_hispanic_val + annual_weights_non_hisp_val
    assert(total_eth_sum == total_gender),'Person Hispanic , Non-Hisp sum validation with Annual weights failed, exiting now...'
    
    # Populating specific values to cells
    rep_UE_per_sht.range('M43').value = annual_weights_hispanic_val
    rep_UE_per_sht.range('M44').value = annual_weights_non_hisp_val
    rep_UE_per_sht.range('M46').value = total_eth_sum
    rep_UE_per_sht.range('M47').value = ''
    
    # Updating values from SLD UE for Hispanic identity of HH
    rep_UE_per_sht.range('A121:L128').options(index=False,header=None).value = language_df
    '''
    annual_wts_only_spanish_val = per_weights_orig_df[per_weights_orig_df[0] == 'Only Spanish'][2].values[0]
    annual_wts_mostly_spanish_val = per_weights_orig_df[per_weights_orig_df[0] == 'Mostly Spanish'][2].values[0]
    annual_wts_spanish_eng_val = per_weights_orig_df[per_weights_orig_df[0] == 'Spanish & English'][2].values[0]
    annual_wts_mostly_english_val = per_weights_orig_df[per_weights_orig_df[0] == 'Mostly English'][2].values[0]
    annual_wts_only_english_val = per_weights_orig_df[per_weights_orig_df[0] == 'Only English'][2].values[0]
    '''
    
    annual_wts_only_spanish_val = per_weights_orig_df[per_weights_orig_df[0] == 'Only Spanish'][1].values[0]
    annual_wts_mostly_spanish_val = per_weights_orig_df[per_weights_orig_df[0] == 'Mostly Spanish'][1].values[0]
    annual_wts_spanish_eng_val = per_weights_orig_df[per_weights_orig_df[0] == 'Spanish & English'][1].values[0]
    annual_wts_mostly_english_val = per_weights_orig_df[per_weights_orig_df[0] == 'Mostly English'][1].values[0]
    annual_wts_only_english_val = per_weights_orig_df[per_weights_orig_df[0] == 'Only English'][1].values[0]
    
    
    
    rep_UE_per_sht.range('M121').value = annual_wts_only_spanish_val
    rep_UE_per_sht.range('M122').value = annual_wts_mostly_spanish_val
    rep_UE_per_sht.range('M123').value = annual_wts_spanish_eng_val
    rep_UE_per_sht.range('M124').value = annual_wts_mostly_english_val
    rep_UE_per_sht.range('M125').value = annual_wts_only_english_val
    rep_UE_per_sht.range('M126').value = annual_weights_non_hisp_val
    lang_total = annual_wts_only_spanish_val + annual_wts_mostly_spanish_val + annual_wts_spanish_eng_val + annual_wts_mostly_english_val + annual_wts_only_english_val + annual_weights_non_hisp_val
    assert(lang_total == total_gender),'Person Langugae sum validation with Annual weights failed, exiting now...'
    rep_UE_per_sht.range('M128').value = lang_total
    
    
    # Reading data from "RAW UEs for Upload_NNR" Person sheet
    raw_UE_upload_sht = wb_e_Per.sheets['Raw UEs for Upload_NetRatings']
    
    # Date(MMDDYYYY) in column H
    raw_UE_upload_sht.range('H1:H100').value = '%s01%s'%(num_month,annual_year)
    # Creating dataframe for "RAW UEs for Upload_NNR" sheet
    raw_UE_upload_df = raw_UE_upload_sht.range('A1:J100').options(pd.DataFrame,header=0,index=False).value

    raw_UE_upload_df[2] = raw_UE_upload_df[2].str.strip()
    
    print('\n#################################################################')
    print('Validating Person Adjusted sum for "Raw UEs for Upload_NetRatings" sheet in e_Persons2+_mmyyy.xlsx')
    print('#################################################################\n')
    # Getting GenderAge Categories values
    per_gen_val = list(raw_UE_upload_df[raw_UE_upload_df[2] == 'GenderAge'][6])
    per_gen_adj_val = get_adjusted_values(per_gen_val)
    per_gen_adj_val_sum = round(sum(per_gen_adj_val),2)
    print('Person GenderAge Adjusted Sum: ',per_gen_adj_val_sum)
    assert(per_gen_adj_val_sum == 100),'Person GenderAge Adjusted Sum for RAW UEs for Upload sheet failed, exiting now...'
    raw_UE_upload_sht.range('I1').options(transpose=True).value = per_gen_adj_val

    # Getting Person EducationHOH Categories values
    per_edu_of_hoh_val = list(raw_UE_upload_df[raw_UE_upload_df[2] == 'EducationHOH'][6])
    per_edu_of_hoh_adj_val = get_adjusted_values(per_edu_of_hoh_val)
    per_edu_of_hoh_adj_sum = round(sum(per_edu_of_hoh_adj_val),2)
    print('Person EducationofHOH Adjusted Sum: ',per_edu_of_hoh_adj_sum)
    assert(per_edu_of_hoh_adj_sum == 100),'Person EducofHOH adjusted sum for RAW UEs for Uploa sheet failed, exiting now...'
    raw_UE_upload_sht.range('I31').options(transpose=True).value = per_edu_of_hoh_adj_val
    
    # Getting Person HispanicHOH Categories values
    per_hisp_hoh_val = list(raw_UE_upload_df[raw_UE_upload_df[2] == 'HispanicHOH'][6])
    per_hisp_hoh_adj_val = get_adjusted_values(per_hisp_hoh_val)
    per_hisp_hoh_adj_sum = round(sum(per_hisp_hoh_adj_val),2)
    print('Person Hispanic HOH Adjusted Sum: ',per_hisp_hoh_adj_sum)
    assert(per_hisp_hoh_adj_sum == 100),'Person Hispanic HOH adjusted sum for RAW UEs for Upload sheet failed, exiting now...'
    raw_UE_upload_sht.range('I35').options(transpose=True).value = per_hisp_hoh_adj_val
    
    # Getting Person SpanishLanguageDominance Categories values
    per_spanish_lang_val = list(raw_UE_upload_df[raw_UE_upload_df[2] == 'SpanishLanguageDominance'][6])
    per_spanish_lang_adj_val = get_adjusted_values(per_spanish_lang_val)
    per_spanish_lang_adj_sum = round(sum(per_spanish_lang_adj_val),2)
    print('Person Spanish Language Adjusted Sum: ',per_spanish_lang_adj_sum)
    assert(per_spanish_lang_adj_sum == 100),'Person Spanish Language adjusted sum for RAW UEs for Upload sheet failed, exiting now...'
    #raw_UE_upload_sht.range('I37').options(transpose=True).value = hh_hhsize_adj_val
    raw_UE_upload_sht.range('I37').options(transpose=True).value = per_spanish_lang_adj_val
    
    # Getting Person State Categories values
    per_state_val = list(raw_UE_upload_df[raw_UE_upload_df[2] == 'State'][6])
    per_state_adj_val = get_adjusted_values(per_state_val)
    per_state_adj_sum = round(sum(per_state_adj_val),2)
    print('Person State Adjusted Sum: ',per_state_adj_sum)
    assert(per_state_adj_sum == 100),'Person State adjusted sum for RAW UEs for Upload sheet failed, exiting now...'
    raw_UE_upload_sht.range('I43').options(transpose=True).value = per_state_adj_val
    
    
    
    # Reading data from Person FTP sheet and saving it to PersonsUEs_190101.csv
    per_ftp_sht = wb_e_Per.sheets['FTP']
    per_ftp_df = per_ftp_sht.range('A1:H100').options(pd.DataFrame,header=0,index=False).value
    per_ftp_df.to_csv(output_path + '//' + 'PersonsUEs_%s%s01.csv'%(last_2_digit_year,num_month),index=False,header=None)   
    
    wb_e_Per.save(output_path + '//' + 'e_Persons2+_%s%s.xlsx'%(month,last_2_digit_year))
    wb_e_Per.close()
    print('\n#################################################################')
    print('Person Validation completed successfully!!!')
    print('#################################################################')
    print('\nHome UEs completed successfully!!!')
    #######################################################
    # e_Persons2+_mmmyy.xlsx Workbook Section Ends
    #######################################################
else:
    print('\nWeights Validtion Failed, Exiting now...')
    print('\nPlease use correct weights and run the script again.')
