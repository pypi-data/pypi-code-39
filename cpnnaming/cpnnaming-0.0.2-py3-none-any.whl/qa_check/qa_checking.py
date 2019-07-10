#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 11:41:57 2019

@author: jennywang
"""
import psycopg2
import pandas as pd
import pandas.io.sql as sqlio
import numpy as np
from collections import defaultdict

from cpnnaming.retrieve_data import cntdb
import gs2df

'''STEP 1: Retrive Rules from Google Sheet'''

# retrieve information from google sheet using API
  # used a different google sheet from "Campaign Naming Convention". the new google sheet only contains rules 
  # the new google sheet is synced with the original google sheet, so does not require mannual edit when rules are changed

rules=gs2df.gs2df('client_secret_540551931166-21q6c10ctr74s4t9d83j1muknjvuoo69.apps.googleusercontent.com.json',
                  'Campaign Naming Rules')

# creating rules from google sheet
UDS = rules[0]["UDS"].values.tolist()
EDL = rules[1]["EDL"].values.tolist()
CLNT = rules[2]["client_short_name"].values.tolist()
PRD = rules[3]["PRD"].values.tolist()
matching = rules[4] # macthing channels with tactics
BNM = rules[5]["Brand/Non/Comp"].values.tolist()
CRI = rules[6]["Criterion Type"].values.tolist()
NLT = rules[7]["NLT"].values.tolist()
CNT = rules[8]["Country"].values.tolist()
LNG = rules[9]["Language"].values.tolist()
ENG = rules[10]["Engine"].values.tolist()

# matching channels and tactics
CHNL_TACT = defaultdict(list)

for index, row in matching.iterrows():
    CHNL_TACT[row["CHNL"]].append(row["TACT"])
    
# NOTES: if there is any change in rules, just update the individual QA_test function
QA1 = []
QA2 = []
QA3 = []
QA4 = []
QA5 = []
QA6 = []
QA7 = []
QA8 = []
QA9 = []
QA10 = []
QA11 = [] 
result = []

    
'''STEP 2: Retrieve QA Data Set & Define QA Rules'''

class QA_CHECKING:
    
    def get_data(schema, table):
        data_qa = cntdb.retrieve_table(schema, table)
        return data_qa

# NOTES: if there is any change in rules, just update the individual QA_test function

    #QA1: Check underscores numbers
    def QA1_test(lst):
        if len(lst) == UDS[0]:
            QA1.append(0)
        else:
            QA1.append(1)
        
        return QA1

    #QA2: Check EDL
    def QA2_test(a, lst):
        if lst[a] in EDL:
            QA2.append(0)
        else:
            QA2.append(1)
        
        return QA2 

    #QA3: Check client short name
    def QA3_test(a, lst):
        if lst[a] in CLNT:
            QA3.append(0)
        else:
            QA3.append(1)
        
        return QA3

    #QA4: Check product name
    def QA4_test(a, lst):
        if len(lst[a].split("-"))<=PRD[0] or "-" not in lst[a]:
            QA4.append(0)
        else:
            QA4.append(1)
        
        return QA4

    #QA5: Check whether Channel and tactic match
    def QA5_test(a, lst):
        if lst[a] in CHNL_TACT and lst[a+1] in CHNL_TACT.get(lst[a]):
            QA5.append(0)
        else: 
            QA5.append(1)

        return QA5

    #QA6: Check Brand/Non/Comp 
    def QA6_test(a, lst):
        if lst[a] in BNM:
            QA6.append(0)
        else:
            QA6.append(1)
    
        return QA6

    #QA7: Check criterion type
    def QA7_test(a, lst):
        if lst[a] in CRI:
            QA7.append(0)
        else:
            QA7.append(1)

        return QA7

    #QA8: Check NLT
    def QA8_test(a, lst):
        if len(lst[a].split("-"))<=NLT[0] or "-" not in lst[a]:
            QA8.append(0)
        else:
            QA8.append(1)

        return QA8

    #QA9: Check country
    def QA9_test(a, lst):
        if lst[a] in CNT:
            QA9.append(0)
        else:
            QA9.append(1)
        
        return QA9

    #QA10: Check language
    def QA10_test(a, lst):
        if lst[a] in LNG:
            QA10.append(0)
        else:
            QA10.append(1)
        
        return QA10

    #QA11: Check target engine 
    def QA11_test(a, lst):
        if lst[a] in ENG:
            QA11.append(0)
        else:
            QA11.append(1)

        return QA11

    # QA Check function 
    def QA_check(df):
        for i in range(len(df["campaign"])):
            
            lst = df["campaign"][i].split("_")
            QA_CHECKING.QA1_test(lst)
            a = 0
            QA_CHECKING.QA2_test(a,lst)
            a += 1
            QA_CHECKING.QA3_test(a,lst)
            a += 1
            QA_CHECKING.QA4_test(a,lst)
            a += 1
            QA_CHECKING.QA5_test(a,lst)
            a += 2
            QA_CHECKING.QA6_test(a,lst)
            a += 1
            QA_CHECKING.QA7_test(a,lst)
            a += 1
            QA_CHECKING.QA8_test(a,lst)
            a += 1
            QA_CHECKING.QA9_test(a,lst)
            a += 1
            QA_CHECKING.QA10_test(a,lst)
            a += 1
            QA_CHECKING.QA11_test(a,lst)   
        
            QA = QA1[i]+QA2[i]+QA3[i]+QA4[i]+QA5[i]+QA6[i]+QA7[i]+QA8[i]+QA9[i]+QA10[i]+QA11[i]
            if QA == 0:
                result.append("Passed")
            else:
                result.append("Failed")
            
   # NOTES: for each campaign name, the dataframe reports: 
       # the overall result - "Passed" OR "Failed" 
       # AND the QA result for each case
   
        df["Result"] = np.array(result)
        df["Undersocre Numbers"] = np.array(QA1)
        df["EDL"] = np.array(QA2)
        df["Client Short Name"] = np.array(QA3)
        df["Product Name"] = np.array(QA4)
        df["Channel & Tactic"] = np.array(QA5)
        df["Brand/Non/Comp"] = np.array(QA6)
        df["Criterion Type"] = np.array(QA7)
        df["NLT"] = np.array(QA8)
        df["Country"] = np.array(QA9)
        df["Language"] = np.array(QA10)
        df["Engine"] = np.array(QA11)
        df_failed = df[df["Result"]=="Failed"] # filter out failed result
        df_failed = df_failed.reset_index(drop=True)
        print(df_failed)
        return df_failed


'''STEP 3: Perform QA_Check and Return Failed Result'''

if __name__ == "__main__":
    schema = "public" 
    table = ".a_20190617_4298634304_campaign_performance_report" # need naming template for the datatable
    data_qa = QA_CHECKING.get_data(schema, table)
    print("Successfully Retrieved Data!")
    QA_CHECKING.QA_check(data_qa)
    print("Successfully Performed QA Check!")
    #result_table(data_qa)
    #print("Successfully Stored Result")
    #failed_df = data_qa[data_qa["Result"]=="Failed"] # filter out failed result
    #failed_df = failed_df.reset_index(drop=True) # store failed result
    print("Successfully Returned Failed Campaign Names!")
    
    
