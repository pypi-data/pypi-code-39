import pandas as pd
import csv

''' This is a python module for the online learning community.'''
df_blp = pd.read_csv("./csv/learning_path_bus.csv",encoding='utf-8')
df_clp = pd.read_csv('./csv/learning_path_cre.csv', encoding='utf-8')
df_tlp = pd.read_csv('./csv/learning_path_tech.csv', encoding='utf-8')
def bus_llp_csv():
    '''This is a method that returns a CSV file of all the learning paths in the business category.'''
    return(df_blp)

def bus_llp_courses():
    '''This is a method that returns a list of all the learning paths in the business category.'''
    return(df_blp['name'].tolist())

def bus_llp_skills():
    '''This is a method that returns a list of all the skills in the business category.'''
    return(df_blp.groupby('skills').count().index.tolist())

def bus__llp_dict():
    '''This is a method that returns a dictionary of skills and their learning paths in the business category.'''
    return(df_blp.groupby('skills')['name'].apply(list).to_dict())

def cre_llp_csv():
    '''This is a method that returns a CSV file of all the learning paths in the creative category.'''
    return(df_clp)

def cre_llp_courses():
    '''This is a method that returns a list of all the learning paths in the creative category.'''
    return(df_clp['name'].tolist())

def cre_llp_skills():
    '''This is a method that returns a list of all the skills in the creative category.'''
    return(df_clp.groupby('skills').count().index.tolist())

def cre_llp_dict():
    '''This is a method that returns a dictionary of skills and their learning paths in the creative category.'''
    return(df_clp.groupby('skills')['name'].apply(list).to_dict())

def tech_llp_csv():
    '''This is a method that returns a CSV file of all the learning paths in the creative category.'''
    return(df_tlp)

def tech_llp_courses():
    '''This is a method that returns a list of all the learning paths in the creative category.'''
    return(df_tlp['name'].tolist())

def tech_llp_skills():
    '''This is a method that returns a list of all the skills in the creative category.'''
    return(df_tlp.groupby('skills').count().index.tolist())

def tech_llp_dict():
    '''This is a method that returns a dictionary of skills and their learning paths in the creative category.'''
    return(df_tlp.groupby('skills')['name'].apply(list).to_dict())
