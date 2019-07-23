import sys
import os

try:
    from pyfission.configs.config import *
except ImportError:
    sys.exit(1)


"""
DWH Creds Structure:
:key = db type
:value = dict
    :key = database/project name
    :value = dict
        :key = host, port, database, user, password 
        
        # for BigQuery
        :key = private_key file location, project, bucket, dataset
"""
dwh_creds = {'redshift': {},
             'bigquery': {
             },
             'mysql': {
             },
             'mssql': {},
             'postgres': {},
             'oracle': {},
             }

# S3
s3_access_key = ''
s3_secret_key = ''
s3_bucket_data = ''

# change python execution env
python_exec = 'python'
