#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 13:15:17 2019

@author: jennywang
"""
import psycopg2
from sqlalchemy import create_engine
from datetime import date
from cpnnaming.qa_check import qa_checking

# Define function to upload the result dataset 
def upload_table(schema, campaign_name, df):
    connection = psycopg2.connect(user="interns",
                                  password="Evolve3100",
                                  host="34.67.217.53",
                                  port="5432",
                                  database="postgres")
    cursor = connection.cursor()

    if len(df) != 0:
        table_name = "{}{}" #table name template TBD
        engine = create_engine('postgresql://interns:Evolve3100@34.67.217.53:5432/postgres')
        df.to_sql(table_name.format(NAME, DATE), engine, if_exists = 'replace',index = False)
        
        connection.commit()
        connection.close()
        cursor.close()
        print("Successfully Uploaded the Result!")
        
    else:
        print("Upload Failed!")
        

if __name__ == "__main__":
    schema = "public" 
    table = ".a_20190617_4298634304_campaign_performance_report" # Naming Template TBD
    NAME = "Incorrect Campaign Naming"
    DATE = date.today()
    df = qa_checking.QA_CHECKING.get_data(schema, table)
    print("Data Retrieved!")
    failed_df = qa_checking.QA_CHECKING.QA_check(df)
    print("QA Checked!")
    #failed_df = qa_checking.result_table(qa_data)
    #print("Found failed!")
    upload_table(schema, table, failed_df)
    print("Result Uploaded!")



