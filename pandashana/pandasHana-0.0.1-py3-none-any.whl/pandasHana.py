import pandas as pd
import json
#import pyhdb
from hdbcli import dbapi
import datetime
import math
import logging
import re
from pprint import pprint, pformat

import tprogress

logger = logging.getLogger('dfsql')
logger.setLevel(logging.INFO)

class PandasHana :

    nvchar_len = 255
    nvchar_list = {10:15,40:50,70:100,200:255}
    # Not used due to SAC issues
    maptypes_direct = {'int8': 'TinyINT', 'int16': 'SMALLINT', 'int32': 'Integer', 'int64': 'BIGINT', 'float32': 'REAL',
                'float64': 'DOUBLE', 'date': 'DATE','str': 'NVARCHAR' + '(' + str(nvchar_len) + ')',
                'datetime64[ns]':'TIMESTAMP','bool':'BOOLEAN'}
    maptypes_simple = {'int8': 'Integer', 'int16': 'Integer', 'int32': 'Integer', 'int64': 'BIGINT', 'float32': 'DECIMAL',
                'float64': 'DECIMAL', 'date': 'DATE', 'str': 'NVARCHAR' + '(' + str(nvchar_len) + ')',
                'datetime64[ns]': 'TIMESTAMP', 'bool': 'BOOLEAN'}

    map_code_types = {1:'int8',3:'int32',4:'int64',5:'float64',6:'float32',7:'float64',11:'object',28:'bool'}

    def __init__(self) :
        pass

    def connect(self,host,port,user,password,autocommit=True):
        logger.info("Connect to " + host + ":" + str(port) + "   user: " + user + "   password: ******")
        self.connection = dbapi.connect(address=host, port=port, user=user, password=password, autocommit=autocommit,
                                        packetsize=1000)
    def get_connection(self):
        return self.connection

    def map_panda_dtypes(self, dseries,ist,datetime2date=False,map_dict='D'):
        dt = str(dseries.dtype)
        if dt == 'object':
            dt = 'date' if isinstance(ist, datetime.date) else 'str'
        elif dt == 'datetime64[ns]' and datetime2date:
            dt = 'date'
        if dt is 'str' :
            max = dseries.str.len().max()
            for key,value in self.nvchar_list.items() :
                if max <= key :
                    return 'NVARCHAR' + '(' + str(value) + ')'
            return 'NVARCHAR' + '(' + str(max+10) + ')'
        else :
            if map_dict == 'S' :
                return self.maptypes_simple[dt]
            elif map_dict == 'D' :
                return self.maptypes_direct[dt]
            else :
                logger.warning("Unknown mapping dict '{}', usind 'D'".format(map_dict))
                return self.maptypes_direct[dt]



    def get_column_types(self,df,map_dict):
        cdf = df.reset_index()
        col_types = list()
        for col in cdf.columns:
            hanatype = self.map_panda_dtypes(df[col], df[col].iloc[0], map_dict=map_dict)
            col_types.append({'name':col.upper(),'type':hanatype})
        return col_types

    def check_table_exist_sql(self,table, schema):
        sqltest = "SELECT TABLE_NAME FROM  SYS.TABLES WHERE  SCHEMA_NAME = '" + schema + "' AND TABLE_NAME LIKE '%" + table + "%' ;"
        logger.info("Test Table exist SQL: " + sqltest)
        return sqltest

    def check_table_exist(self,table, schema,keep_open=False):
        sql_string = self.check_table_exist_sql(table, schema)
        cursor = self.connection.cursor()

        logger.info("SQL Statement: " + sql_string)
        result = cursor.execute(sql_string)

        table_exists = False if cursor.fetchone() is None else True

        if not keep_open:
            self.connection.close()

        return table_exists

    def drop_table_sql(self,table,schema):
        tablename = "\"" + table + "\""
        schemaname = '\"' + schema + "\""
        sql_drop_table = "DROP TABLE " + schemaname + "." + tablename + ';'
        logger.info("Drop Table SQL: " + sql_drop_table)
        return sql_drop_table

    def drop_table(self,table,schema,keep_open=False):
        sql = self.drop_table_sql(table,schema)
        self.execute_sql(sql, keep_open=keep_open)

    def create_table_sql(self,df,table,schema,ignore_index = False,datetime2date=False,map_dict='D'):
        tablename = "\"" + table + "\""
        schemaname = '\"' + schema + "\""

        key_fields = list(df.index.names)

        sql = "CREATE COLUMN TABLE " + schemaname + "." + tablename + '('
        columnkey = list()
        if key_fields and key_fields[0] is not None and ignore_index == False:
            for i in key_fields:
                indexvalues = df.index.get_level_values(i)
                ist = indexvalues[0]
                hanatype = self.map_panda_dtypes(indexvalues, ist, datetime2date=datetime2date, map_dict=map_dict)
                ck = '\"' + i.upper() + '\"'
                columnkey.append(ck)
                sql += ' ' + ck + ' ' + hanatype + ' NOT NULL ,'

        for col in df.columns:
            logger.debug("Column for dtype: {}".format(col))
            hanatype = self.map_panda_dtypes(df[col], df[col].iloc[0], map_dict=map_dict)
            logger.debug("Dtype: {}".format(hanatype))
            column = '\"' + col.upper() + '\"'
            sql += ' ' + column + ' ' + hanatype + ' , '
            ### reformat datetime
            if hanatype == 'TIMESTAMP':
                df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d %H:%M:%S')
        if key_fields and key_fields[0] is not None and ignore_index == False:
            sql += " PRIMARY KEY("
            for c, i in enumerate(key_fields):
                sql += columnkey[c] + " , "
            sql = sql[:-2] + ")"
        else:
            sql = sql[:-2]
        sql += ");"

        logger.info("Create Table SQL: "  + sql)
        return sql

    def create_table(self,df,table,schema,ignore_index = False,datetime2date=False,map_dict='D',keep_open=False):
        sql = self.create_table_sql(df,table,schema,ignore_index = ignore_index,datetime2date=datetime2date,map_dict=map_dict)
        self.execute_sql(sql, keep_open=keep_open)

    def truncate_table_sql(self,table,schema):
        tablename = "\"" + table + "\""
        schemaname = '\"' + schema + "\""
        sql = "TRUNCATE TABLE " + schemaname + "." + tablename
        logger.info("Truncate table SQL: " + sql)
        return sql

    def truncate_table(self,table,schema,keep_open=False):
        sql = self.truncate_table_sql(table,schema)
        self.execute_sql(sql,keep_open=keep_open)

    def insert_sql(self,df,table,schema,ignore_index=False):
        tablename = "\"" + table + "\""
        schemaname = '\"' + schema + "\""
        key_fields = list(df.index.names)

        if key_fields and key_fields[0] is not None and ignore_index==False:
            vlist =(" VALUES("+(len(df.columns) + len(key_fields))* "?,")[:-1]+")"
        else :
            vlist = (" VALUES(" + len(df.columns) * "?,")[:-1] + ")"

        sql = "INSERT INTO " + schemaname + "." + tablename + vlist
        logger.debug("INSERT SQL : " + sql)
        return sql

    def insert_only(self,df,table,schema,ignore_index=False,package_size = None,keep_open=False):
        sql = self.insert_sql(df,table,schema,ignore_index=ignore_index)

        ## slicing DF in chunks of chunksize
        if not package_size:
            package_size = len(df.index)
        elif package_size <= 1.0:
            package_size = math.ceil(len(df.index) * package_size)

        key_fields = list(df.index.names)
        cursor = self.connection.cursor()

        time_insert_p = tprogress.progress()
        for i in range(0, df.shape[0], package_size):
            if key_fields and key_fields[0] is not None and ignore_index == False:
                datatable = df.iloc[i:i + package_size].to_records(index=True).tolist()
            else:
                datatable = df.iloc[i:i + package_size].to_records(index=False).tolist()

            try:
                cursor.executemany(sql, datatable)
            except dbapi.IntegrityError as i_error:
                logger.error(i_error)
                logger.error("First record : " + pformat(datatable[0]))
            except dbapi.ProgrammingError as p_error:
                logger.error(p_error)
                logger.error("First record : " + pformat(datatable[0]))

            logger.debug("Insert: {}/{}  {}".format(i, df.shape[0], time_insert_p.elapsed_time()))

        if not keep_open :
            self.connection.close()

    # datetime2date only considered for indices. For columns types has to be converted to date first.
    def insert(self, df, table, schema, mode='a', ignore_index=False, package_size=None, datetime2date=False, \
               map_dict='D',keep_open=False):

        if df.empty :
            logger.warning("Empty Dataframe")
            return

        ### test: table exists in db
        table_exists = self.check_table_exist(table,schema,keep_open=True)

        if table_exists and mode is 'c' :
            self.drop_table(table,schema,keep_open=True)
            table_exists = False

        if not table_exists :
            self.create_table(df,table,schema,ignore_index = ignore_index,datetime2date=datetime2date,map_dict=map_dict,keep_open=True)

        ### Mode 'w' leads to remove data of table
        if mode == 'w' and table_exists :
            self.truncate_table(table,schema,keep_open=True)

        self.insert_only(df,table,schema,ignore_index=ignore_index,package_size = package_size,keep_open=keep_open)


    def execute_sql(self,sql_string,keep_open=False):
        cursor = self.connection.cursor()
        logger.info("SQL Statement: " + sql_string)
        result = cursor.execute(sql_string)
        if not keep_open :
            self.connection.close()
        return result

    def update(self,sql_string,keep_open=False):
        cursor = self.connection.cursor()
        logger.info("SQL Statement: " + sql_string)
        cursor.execute(sql_string)
        if not keep_open :
            self.connection.close()

    def select(self,sql,return_type ='JSON',num_rec_sql=None,column_names=None,fetch = "direct",frac=0.1):
        cursor = self.connection.cursor()

        num_rec = None
        if num_rec_sql :
            logger.info("SQL SELECT: " + num_rec_sql)
            cursor.execute(num_rec_sql)
            num_rec = cursor.fetchone()[0]
            limit = re.search('LIMIT\s+(\d+)',sql)
            if limit :
                limit = int(limit.group(1))
                num_rec = limit if limit < num_rec else num_rec
                logger.info("Number of records to be loaded: {}".format(num_rec))

        logger.info("SQL SELECT: " + sql)
        time_sql = tprogress.progress()
        cursor.execute(sql)
        logger.info("Server processing time (SQL): " + time_sql.elapsed_time())

        time_fetch = tprogress.progress()
        data = list()
        row_package = 1000 if not num_rec else int(num_rec * frac)
        cursor.setfetchsize(row_package)

        if fetch == 'many' :
            time_fetch_package= tprogress.progress()
            rows = cursor.fetchmany()
            while rows :
                data.extend(rows)
                logger.debug("Fetched records: {}/{}  {}".format(len(data), num_rec, time_fetch_package.elapsed_time()))
                rows = cursor.fetchmany(row_package)
        elif fetch == "all" :
            data = cursor.fetchall()
        else :
            for rows in cursor :
                data.append(rows)

        logger.info("Server processing time (Fetch): " + time_fetch.elapsed_time())

        #column_types = [key[1] for key in cursor.description] # not used yet
        if not column_names  :
            column_names = [key[0] for key in cursor.description]
        col_dtypes = {key[0]:key[1] for key in cursor.description}

        logger.debug("Table info from cursor (column name, dtype): \n" + pformat(col_dtypes))

        if 'JSON_RECORDS' in return_type :
            data_dict = [dict(zip(column_names, row)) for row in data]
            data_j = [json.dumps(row) for row in data_dict]
            #return json.dumps(data_dict)
            return data_j
        elif 'DICT_RECORDS' in return_type :
            return [dict(zip(column_names, row)) for row in data]
        elif 'JSON_COLUMNS' in return_type:
            return pd.DataFrame(data,columns=column_names).to_json()
        elif 'PANDAS' in return_type:
            df = pd.DataFrame(data,columns=column_names)
            for col,ctype in col_dtypes.items() :
                if ctype == 14 :
                    df[col] = pd.to_datetime(df[col]).dt.date     # date
                elif ctype == 16 :
                    df[col] = pd.to_datetime(df[col])
                else :
                    try :
                        df[col] = df[col].astype(self.map_code_types[ctype]) # datetime
                    except KeyError as k_error :
                        logger.error("{}: column {} ".format(k_error, col))
            return df
        elif 'COL_LISTS' :
            return list(map(list, zip(*data)))
        elif 'RAW' in return_type:
            return data
        else :
            logger.warning('ERROR Unknown return type: {}' + return_type)

    def close (self) :
        self.connection.close()

def test_sql() :
    # TEST SQL
    host = "10.47.7.174"
    port = 30015
    user = 'RETAILPKG'
    pwd = 'RetPack1'
    sql_select = "SELECT \"CATEGORY_ID\", \"ORDER_SHARE\""
    sql_from = "FROM \"_SYS_BIC\".\"supplier_portal.dh/BASKET\" ('PLACEHOLDER\' = ('$$P_YEAR1$$','2016\'),'PLACEHOLDER' = ('$$P_MONTH2$$','12'),'PLACEHOLDER' = ('$$P_MONTH1$$','1'),'PLACEHOLDER' = ('$$P_YEAR2$$','2018'),'PLACEHOLDER' = ('$$P_LOCATION1$$','0001'),'PLACEHOLDER' = ('$$P_LOCATION2$$','9999'))"
    sql_where = "WHERE \"ORDER_SHARE\" > 0 LIMIT 10;"

    sql = sql_select + " " + sql_from + " " + sql_where
    print (sql)

    #def get_order_share(cat_ids,hana_view,year_from, year_to,month_from,month_to,location_1,location_2) :

    hdb = PandasHana(host, port, user, pwd)
    res = hdb.execute_sql(sql)

    for loc,prob in res :
        print("{} : {}".format(loc,prob))