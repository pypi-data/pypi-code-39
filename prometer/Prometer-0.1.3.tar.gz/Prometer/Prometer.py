#!/usr/bin/env python3
import requests
import json
import math
import pandas as pd
import numpy as np
from operator import add 
from statistics import mean 
from datetime import datetime, timedelta

def performance_issue(df):
    issue_score = df.assign(issue_score = df['Issue Total'] / df['Issue Total'].mean())
    return issue_score.round(3)

def performance_pull(df):
    pull_score = df.assign(pull_score = df['PR Total'] / df['PR Total'].mean())
    return pull_score

def performance_commit(df):
    commit_score = df.assign(commit_score = df['Commit Total'] / df['Commit Total'].mean())
    return commit_score



def performance_LOC(df):
    
    loc_score = df.assign(loc_score = df['LOC Total'] / df['LOC Total'].mean())
    return loc_score

def Total(week):

    for i in range(week):
        issue_csv = pd.read_csv('E:/Materi Kuliah/Semester 8/TA II/!!SIDANG/Revisi/v.03/Hasil/Issue/Derivative/issue_score_week{counter}.csv'.format(counter = i+1), engine='python')
        pr_csv = pd.read_csv('E:/Materi Kuliah/Semester 8/TA II/!!SIDANG/Revisi/v.03/Hasil/Pull/Derivative/PR_score_week{counter}.csv'.format(counter = i+1), engine='python')
        commit_csv = pd.read_csv('E:/Materi Kuliah/Semester 8/TA II/!!SIDANG/Revisi/v.03/Hasil/Commit/Derivative/commit_score_week{counter}.csv'.format(counter = i+1), engine='python')
        loc_csv = pd.read_csv('E:/Materi Kuliah/Semester 8/TA II/!!SIDANG/Revisi/v.03/Hasil/LOC/Derivative/LOC_score_week{counter}.csv'.format(counter = i+1), engine='python')

        mergeIPR = pd.merge(commit_csv,loc_csv, on='User Name', how='outer')
        mergeData = pd.merge(pd.merge(issue_csv,pr_csv, on='User Name'), mergeIPR, on='User Name', how='outer')
        mergeData.fillna(0,inplace = True)
        mergeData['Total Performance of Developer'] = mergeData['issue_score'] + mergeData['pull_score'] + mergeData['commit_score'] + mergeData['loc_score']
        save = mergeData.to_csv(r'E:/Materi Kuliah/Semester 8/TA II/!!SIDANG/Revisi/v.03/Hasil/Performance/Performance_Week-{counter}.csv'.format(counter = i+1), index = None, header= True)
        
    return