import os
import re
import json
import pandas as pd
import mysql.connector as sql
from altoshift.tools import Tools
from pandas.io.json import json_normalize

helper = Tools()

class Mysql():
    @classmethod
    def __init__(self, **kwargs):
        args = kwargs
        self.host = args.get('host','localhost')
        self.username = args.get('username','root')
        self.password = args.get('password','')
        self.database = args.get('database','alto')
        self.conn = sql.connect(host=self.host, database=self.database, user=self.username, password=self.password)

    def readMysql(query):
        df = pd.read_sql(query, con=self.conn)
        resp = df.to_dict(orient='records')
        return resp

if(__name__ == "__main__"):
    print('Believe in Future.')