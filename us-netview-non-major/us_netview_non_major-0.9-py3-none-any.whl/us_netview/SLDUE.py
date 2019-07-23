#import xlwings as xw
#import pandas as pd
#import Lace

# Reading pre-defined Excel Workbook template for creating SLD UE's
path_sld = r'\\nadayisicifs03.dayisi03.enterprisenet.org\share3\SRData\UEData\Internet UEs\SLD UEs\Procedures for Computing Spanish Language UEs_'+prev_month[:3] + prev_month[5:]+'.xlsx'

wb = xw.Book(path_sld)
#wb = xw.Book('Procedures for Computing Spanish Language UEs_Mar19.xls')


# Reading and Updating Calculation sheet
cal_sheet  = wb.sheets['Calculations']

# Getting Monthly Internet Yes and No Cells from e_Persons2+.xlsx book Monthly Universe Estimates sheet
per_total_yes_sum =  rep_UE_per_sht.range('C39').value
per_total_no_sum = rep_UE_per_sht.range('H39').value

# Updating Monthly Internet Yes and No Cells in Calculation sheet
cal_sheet.range('K19').value = per_total_yes_sum
cal_sheet.range('L19').value = per_total_no_sum

# Reading Hispanic and Non-Hispanic value from Calculation sheet
non_hisp_total = cal_sheet.range('J20').value
hisp_total = cal_sheet.range('J21').value

eth_lac_input_df = cal_sheet.range('K6:L7').options(pd.DataFrame,index=False,header=0).value

eth_lacing_out_df = Lace.Lace.Lace2D(2,[per_total_yes_sum,per_total_no_sum],
                                   [non_hisp_total,hisp_total],
                                   eth_lac_input_df.values)

# Updating laced output from K20 cell
cal_sheet.range('K20').options(index=False).value = eth_lacing_out_df


lan_lac_input_df = cal_sheet.range('K8:L12').options(pd.DataFrame,index=False,header=0).value

lan_lacing_out_df = Lace.Lace.Lace2D(2,[cal_sheet.range('K30').value,cal_sheet.range('L30').value],
                                   cal_sheet.range('J31:J35').value,
                                   lan_lac_input_df.values)

# Writing laced dataframe to sheet
cal_sheet.range('K31').options(index=False).value = lan_lacing_out_df

# Reading and Updating Table sheet
tbl_sheet  = wb.sheets['Table']

# Creating Persons in HHs Where Hispanic Identity of the Householder is:
ethnic_df = tbl_sheet.range('A8:L11').options(pd.DataFrame,index=False,header=0).value
ethnic_df[0] = ethnic_df[0].str.strip()

# Creating Hispanic Persons 2+ by Language:
language_df = tbl_sheet.range('A15:L22').options(pd.DataFrame,index=False,header=0).value
language_df[0] = language_df[0].str.strip()

wb.save(path_sld[:86] + 'Procedures for Computing Spanish Language UEs_%s.xlsx'%(curr_month1[:3].upper() + curr_month1[5:]))
wb.close()