import os
from sqlalchemy import create_engine

database_config = r'C:\Users\{}\Documents\db_config.pkl'.format(os.getlogin())
db_types = {'ms': 'Microsoft SQL Server', 'ora': 'Oracle', 'pstg': 'Postgre'}

engine_connection_strings = {'pstg': {'default': 'postgresql://{username}:{password}@{servername}/{databasename}',
                                      'psycopg2': 'postgresql+psycopg2://{username}:{password}@{servername}/{databasename}',
                                      'pg8000': 'postgresql+pg8000://{username}:{password}@{servername}/{databasename}'},

                             'ora': {'default': 'oracle://{username}:{password}@{serverip}:{serverport}/{sidname}',
                                     'cx_oracle': 'oracle+cx_oracle://{username}:{password}@{tnsname}'},

                             'ms': {
                                 'default': 'mssql+pyodbc://{username}:{password}@{dsnname}',
                                 'pymssql': 'mssql+pymssql://{username}:{password}@{serverip}:{serverport}/{databasename}'}
                             }






