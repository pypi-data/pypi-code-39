import os
import re
import json
import pandas as pd
from pandas.io.json import json_normalize

class Tools(object):
    def __init__(self):
        super(Tools, self).__init__()
        
    def writeToCsv(self,fname,df,sep=None):
        df.to_csv(fname, sep=sep, encoding='utf-8', lines=False)
    
    def writeToJson(self,fname,df):
        df.to_json(fname, orient='records', lines=False)

    def readMysqltoJson(self,query,con):
        df = pd.read_sql(query, con=con)
        result = df.to_json(orient='records', lines=False)
        result = json.loads(result.decode('latin-1'))
        return result

    def readXlsToJson(self,file):
        df = pd.read_excel(file)
        result = df.to_json(orient='records', lines=False)
        result = json.loads(result.decode('latin-1'))
        return result

    def readCsvToJson(self,file,xdelimiter=None):
        df = pd.read_csv(file,delimiter=xdelimiter)
        result = df.to_json(orient='records', lines=False)
        result = json.loads(result.decode('latin-1'))
        return result

    def cleanHTMLforJson(self,dt,xfilter=[]):
        df = dt.filter(xfilter) if xfilter else dt
        df = json_normalize(dt)
        for cfilter in xfilter:
            df[cfilter]=re.sub(r'<.+?>','',str(df[cfilter]))
        return df

    def filterJson(self,dt,xfilter=None):
        df = pd.DataFrame(dt)
        df = df.filter(xfilter) if xfilter else df
        result = df.to_json(orient='records', lines=False)
        result = json.loads(result.decode('latin-1'))
        return result

    def slice_per(self, source, step):
        return [source[i::step] for i in range(step)]

    def dataSlicer(self,dt):
        limit=500
        step=((len(dt)/limit)+1)
        result=self.slice_per(dt,step)
        return result

    def altoReader(self,file):
        if(os.path.isfile(file) == False):
            print('File not found')
            return False
        if(file.lower().endswith('.csv')):
            datas = self.readCsvToJson(file)
        elif(file.lower().endswith('.tsv')):
            datas = self.readCsvToJson(file,'\t')
        elif(file.lower().endswith('.xlsx')):
            datas = self.readXlsToJson(file)
        return datas

    def altoOptimizer(self,fname,df2):
        df1 = pd.DataFrame()
        if(os.path.isfile(fname)):
            df2 = pd.read_json(self.readCsvToJson(fname))
        merged = df1.merge(df2, indicator=True, how='outer')
        data = merged[merged['_merge'] == 'right_only']
        self.writeToCsv(fname,df2)
        return data
if(__name__ == "__main__"):
    print('Believe in Future.')