#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 11:37:53 2019

@author: jennywang
"""
import psycopg2
import pandas as pd
import pandas.io.sql as sqlio


'''Step 1: Retrieve Datatable from Server'''

qa_data = pd.DataFrame() # create an empty dataframe to store the qa datatable 

def retrieve_table(schema, table):
    connection = psycopg2.connect(user="interns",
                                  password="Evolve3100",
                                  host="34.67.217.53",
                                  port="5432",
                                  database="postgres")
    cursor = connection.cursor()
    table_name = "{}{}"
    select_query = "select * from " + table_name.format(schema, table)
    #print(select_query)
    campaign_id = sqlio.read_sql_query(select_query, connection)
    
    global qa_data
    qa_data = qa_data.append(campaign_id)
    return qa_data

if __name__ == "__main__":
    schema = "public" 
    table = ".a_20190617_4298634304_campaign_performance_report" # need naming template for the datatable
    qa_data = retrieve_table(schema, table)
    print("Successfully Retrieved Data!")