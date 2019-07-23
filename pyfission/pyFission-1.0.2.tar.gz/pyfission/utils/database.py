import sqlalchemy as sqla
import sys
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import re
import pymysql
from decimal import Decimal
import datetime
import time
from enum import Enum
import cx_Oracle

try:
    import pyodbc
    import pymssql
except ImportError:
    pass

from pyfission.custom_logging.__main__ import func_logger
from pyfission.utils.cloud_google import upload_to_cloud_storage, load_to_table, patch_table_simple as patch_table_simple_bq
from pyfission.utils.file import load_sql, subfolder_path
from pyfission.utils.s3_util import s3_upload_file


def connect_to_database(log, creds, db='mysql', raw=True, **kwargs):
    """
    Returns a connection object - raw/native based on credentials provided and database type
    :param log: logger object
    :param creds: a dictionary object containing credentials necessary for creating the connection object
    :param db: type of database. Acceptable value: [mysql, mssql, oracle, redshift, bigquery]
    :param raw: Boolean flag for type of conection - raw/native
    :param kwargs: dynamic capture of keyword-args
        :param method
        :param host: overrides the host in creds
        :param port: overrides the port in creds
        :param user: overrides the user in creds
        :param password: overrides the password in creds
        :param database: overrides the database in creds
    :return: connection object
    """
    user = creds.get('user', '') if 'user' not in kwargs.keys() else kwargs['user']
    password = creds.get('password', '') if 'password' not in kwargs.keys() else kwargs['password']
    host = creds.get('host', '') if 'host' not in kwargs.keys() else kwargs['host']
    port = creds.get('port', '') if 'port' not in kwargs.keys() else kwargs['port']
    database = creds.get('database', '') if 'database' not in kwargs.keys() else kwargs['database']

    conn = None
    if str(db).lower() == 'mysql':
        port = port if port != '' else '3306'  # Defaults to 3306 is not provided
        if not kwargs.get('method', None) or kwargs['method'] == 'sqlalchemy':
            conn = sqla.create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database))
        elif kwargs['method'] == 'pymysql':
            conn = pymysql.connect(host=host, port=int(port), user=user, password=password, db=database)
        elif kwargs['method'] == 'v8':
            conn = sqla.create_engine('mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(user, password, host, port, database))
        else:
            msg = 'INVALID method in kwargs for db = mysql'
            log.info(msg)
            sys.exit(1)
    elif str(db).lower() == 'mssql':
        if not kwargs.get('method', None) or kwargs['method'] == 'pyodbc':  # TODO: Not Working. fix this
            log.info('Unsupported method. Exiting.')
            sys.exit(1)
            dsn = 'DRIVER=FreeTDS;TDS_VERSION=8.0;SERVER={};PORT={};DATABASE={};UID={};PWD={}'.format(host, port,
                                                                                                      database, user,
                                                                                                      password)
            conn = pyodbc.connect(dsn)
        elif kwargs['method'] == 'pymssql':
            # log.info('Connecting via pymssql.')  # Test Only
            conn = pymssql.connect(server=host, user=user, password=password, database=database)
    elif str(db).lower() in ['postgres', 'redshift']:
        conn = sqla.create_engine("postgresql+psycopg2://{}:{}@{}:{}/{}".format(user, password,
                                                                                host, port,
                                                                                database))
    elif str(db).lower() in ['bigquery']:
        # If it fails try setting the credentials as: export GOOGLE_APPLICATION_CREDENTIALS="path to json"
        try:
            conn = bigquery.Client.from_service_account_json(creds['private_key'])
        except:
            credentials = service_account.Credentials.from_service_account_file(creds['private_key'])
            conn = bigquery.Client(credentials=credentials)
        return conn

    #     else:
    #         return psycopg2.connect(host=host, port=port, user=user, password=password, database=database)
    elif 'oracle' in str(db).lower():
        database = creds.get('servicename', '') if 'database' not in kwargs.keys() else kwargs['database']
        dsn = cx_Oracle.makedsn(host, port, service_name=database)
        return sqla.create_engine('oracle+cx_oracle://{}:{}@{}'.format(user, password, dsn)).raw_connection()
    else:
        log.info('Invalid dbtype selected. Aborting.')
        sys.exit(1)

    if conn:
        if raw:
            return conn.raw_connection()
        else:
            return conn


@func_logger(ignore_kwargs=['query'], ignore_args=[2])
def get_query_results(log, config, query, out_format='df', display_sample=False, **kwargs):
    """
    Wrapper to get results from a DB via provided connection and query
    :param log: logger object
    :param config: config module
    :param query: SQL query for obtaining results
    :param out_format: Acceptable values: df, list
    :param display_sample: Boolean flag to display a sample of output
    :param kwargs: dynamic capture of keyword-args
        :param dbtype: dbtype for config
        :param project: src/project for config
    :return: query results as per out_format, column_names
    """
    _data = None
    _columns = None
    log.info(f"Executing SQL: {query}")
    if out_format == 'list':
        formatted_results = []
        creds = config.dwh_creds[kwargs['dbtype']][kwargs['project']]
        if 'database' in kwargs.keys() and kwargs['database'] is not None:
            creds['database'] = kwargs['database']
        if kwargs['dbtype'] in ['mysql', 'redshift', 'postgres', 'mssql', 'oracle']:
            switcher = {'mysql': {'raw': False, 'method': 'pymysql'},
                        'redshift': {'raw': True, 'method': None},
                        'postgres': {'raw': True, 'method': None},
                        'mssql': {'raw': False, 'method': 'pymssql'},
                        'oracle': {'raw': True, 'method': None},
                        }
            try:
                conn = connect_to_database(log, creds=creds, db=kwargs['dbtype'], raw=switcher[kwargs['dbtype']]['raw'],
                                           method=switcher[kwargs['dbtype']]['method'])
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    results = cursor.fetchall()
                    _columns = [i[0] for i in cursor.description]
            except Exception as e1:
                log.info(f"Error Logged: {e1}. Sleeping and retrying.")
                time.sleep(60)
                conn = connect_to_database(log, creds=creds, db='mysql', raw=False, method='pymysql')
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    results = cursor.fetchall()
                    _columns = [i[0] for i in cursor.description]

            for row in results:
                _temp_row = []
                for _val in row:
                    val = None
                    if type(_val) in [datetime.datetime, str, datetime.date, datetime.time, datetime.timedelta, Enum]:
                        if str(_val) == '0000-00-00 00:00:00':
                            val = '0001-01-01 00:00:00'
                        elif str(_val) == '0000-00-00':
                            val = '0001-01-01'
                        else:
                            val = str(_val)
                    elif type(_val) in [Decimal, float]:
                        val = float(_val)
                    elif type(_val) in [int]:
                        val = int(_val)
                    else:
                        val = _val

                    _temp_row.append(val)
                formatted_results.append(_temp_row)
        # elif kwargs['dbtype'] in ['redshift']: # old
        #     conn = connect_to_database(log, creds=creds, db='redshift', raw=True)
        #     _df = pd.read_sql(query, con=conn, coerce_float=False)
        #     formatted_results = json.loads(_df.to_json(orient='records'))
        else:
            log.info("INVALID kwargs['dbtype']")
            sys.exit(1)

        _data = formatted_results
    elif out_format == 'df':
        creds = config.dwh_creds[kwargs['dbtype']][kwargs['project']] if 'creds' not in kwargs else kwargs['creds']
        if kwargs['dbtype'] in ['mssql']:
            conn = connect_to_database(log, creds=creds, db=kwargs['dbtype'], raw=False, method='pymssql')
        else:
            conn = connect_to_database(log, creds=creds, db=kwargs['dbtype'], raw=True)
        if kwargs['dbtype'] in ['mysql', 'oracle']:
            formatted_results = pd.read_sql(query, con=conn, coerce_float=False)
        elif kwargs['dbtype'] in ['bigquery']:
            formatted_results = pd.read_gbq(query, project_id=creds['project'],
                                            private_key=creds['private_key'], dialect='standard',
                                            configuration=config.bq_config
                                            )
        elif kwargs['dbtype'] in ['redshift', 'postgres', 'mssql']:
            formatted_results = pd.read_sql(query, con=conn, coerce_float=False)
        else:
            log.info("INVALID kwargs['dbtype']")
            sys.exit(1)

        _data = formatted_results
        _columns = _data.columns

    # chunksize = 500_000
    # if out_format == 'df':
    #     log.info(f"Executing SQL: {query}")
    #     if 'chunked' not in kwargs.keys() or not kwargs['chunked']:
    #         if 'db' in kwargs.keys() and kwargs['db']:
    #             if kwargs['db'] == 'bigquery':
    #                 data = pd.read_gbq(query, project_id=kwargs['creds']['project'],
    #                                    private_key=kwargs['creds']['private_key'], dialect='standard',
    #                                    configuration=kwargs['config'].bq_config)
    #             else:
    #                 data = pd.read_sql(query, con=conn, coerce_float=False)
    #         else:
    #             data = pd.read_sql(query, con=conn, coerce_float=False)
    #     else:
    #         if 'db' in kwargs.keys() and kwargs['db'] in ['mysql']:
    #             data = []
    #             _temp_df = pd.read_sql(f"select count(*) as count from ({query.replace(';', '')}) t1;", con=conn)
    #             row_count = int(_temp_df['count'][0])
    #             if row_count <= chunksize:
    #                 data = pd.read_sql(query, con=conn, coerce_float=False)
    #             else:
    #                 total_chunks = int(row_count / chunksize) + 1
    #                 for i in range(total_chunks):
    #                     log.info(f'Processing chunk {i}/{total_chunks}')
    #                     _query = query.replace(';', '') + f" LIMIT {i * chunksize}, {chunksize} ;"
    #                     _data = pd.read_sql(_query, con=conn, coerce_float=False)
    #                     data.append(_data)
    #         else:
    #             # Inefficient chunking
    #             if 'db' in kwargs.keys() and kwargs['db']:
    #                 if kwargs['db'] == 'bigquery':
    #                     data = pd.read_gbq(query, project_id=kwargs['creds']['project'],
    #                                        private_key=kwargs['creds']['private_key'], dialect='standard',
    #                                        configuration=kwargs['config'].bq_config)
    #                 else:
    #                     data = pd.read_sql(query, con=conn, coerce_float=False, chunksize=chunksize)
    #             else:
    #                 data = pd.read_sql(query, con=conn, coerce_float=False, chunksize=chunksize)
    #
    #     try:
    #         conn.close()
    #     except:
    #         pass
    # elif out_format == 'list':
    #     if dbtype_src == 'mysql':
    #         connection = pymysql.connect(host=creds['host'], user=creds['user'], password=creds['password'],
    #                                      db=creds['database'])
    #         with connection.cursor() as cursor:
    #             cursor.execute(query)
    #             result = cursor.fetchall()
    #             field_names = [i[0] for i in cursor.description]
    else:
        log.info('INVALID out_format')
        sys.exit(1)

    if display_sample:
        if isinstance(_data, pd.DataFrame):
            log.info('Columns: {}'.format(list(_data.columns.values)))
            log.info('Shape: {}'.format(_data.shape))
            log.info(_data.head(5))
        elif isinstance(_data, list):
            log.info(_data[:5])
        else:
            log.info('INVALID type for data')
            log.info(_data)
            sys.exit(1)

    return _data, _columns


@func_logger(ignore_kwargs=['sql_query'], ignore_args=[2])
def execute_sql(log, config, sql_query, db, **kwargs):
    """
    Wrapper to get results from a DB via provided connection and query
    :param log: logger object
    :param sql_query: SQL query for obtaining results
    :param db: DB Type
    :param kwargs: dynamic capture of keyword-args
        :param db: database type
        :param creds: Credentials Dict
        :param conn: connection object
        :param project: projectname
        :param split_param: use a different splitter char/set of char - to get around semicolon
    :return: query results as per out_format
    """
    if db == 'bigquery':
        creds = kwargs['creds'] if 'creds' in kwargs.keys() else {}
        split_param = kwargs['split_param'] if 'split_param' in kwargs.keys() else ';'
        queries = list(filter(None, [_q.strip() for _q in sql_query.split(split_param)]))
        if 'CREATE TEMP FUNCTION' in sql_query:
            queries = [sql_query]
        total_processed_bytes = 0.0
        for _query in queries:
            bq_client = connect_to_database(log, creds, db=db, raw=False)

            job_config = bigquery.QueryJobConfig()
            job_config.dry_run = False
            job_config.use_query_cache = True
            job_config.use_legacy_sql = False

            log.info("Executing SQL: {}".format(_query.strip()))
            query_job = bq_client.query(query=_query.strip(), job_config=job_config)
            query_job.result()
            total_processed_bytes += query_job.total_bytes_processed
            log.info("This query processed {} GBs.".format(query_job.total_bytes_processed / (1024.0 ** 3)))
            log.info(f'Processed {query_job.num_dml_affected_rows} records.')
        log.info(f'Whole Query Processed: {total_processed_bytes/(1024.0 ** 3)} GBs')
    elif db == 'redshift':
        sql_secured_ = re.sub('\nCREDENTIALS.*?DELIMITER', '\nCREDENTIALS *HIDDEN* \nDELIMITER', str(sql_query),
                              flags=re.DOTALL)
        sql_secured = re.sub('\nCREDENTIALS.*?json', '\nCREDENTIALS *HIDDEN* \njson', str(sql_secured_),
                             flags=re.DOTALL)
        log.info('Executing SQL: {}'.format(sql_secured))

        conn = connect_to_database(log, creds=config.dwh_creds[db]['bi'], db=db, raw=True)
        cur = conn.cursor()
        if sql_secured.lower().startswith('vacuum'):
            try:
                cur.execute(sql_query)
            except Exception as e1:
                log.info("Error Logged: {}".format(e1))
        else:
            cur.execute(sql_query)
        conn.commit()
        log.info('Finished Executing SQL. Processed {} records.'.format(cur.rowcount))
    elif db == 'mysql':
        sql_secured = sql_query
        log.info('Executing SQL: {}'.format(sql_secured))

        creds = kwargs['creds'] if 'creds' in kwargs.keys() else config.dwh_creds[db][kwargs['project']]

        conn = connect_to_database(log, creds=creds, db=db, raw=True)
        cur = conn.cursor()
        try:
            for _sql_query in filter(None, sql_query.split(';')):
                cur.execute(_sql_query.strip())
        except Exception as e1:
            log.info("Error Logged: {}".format(e1))
            sys.exit(1)
        conn.commit()
        log.info('Finished Executing SQL. Processed {} records.'.format(cur.rowcount))
    else:
        log.info(f'INVALID db: {db}')

    return None


def local_file_to_dwh(log, config, local_file_path, dbtype, project, schema, table, pkeys: list, **kwargs):
    """
    Wrapper to move data from a local file to dwh table.
    Move the data via a raw table, remove matching rows based on pkeys from original table.
    :param log: logger object
    :param config: config module
    :param local_file_path: local file path
    :param dbtype: db type
    :param project: projectname
    :param schema: schema of destination table
    :param table: destination table
    :param pkeys: table columns which determine matching rows
    :param kwargs: dynamic capture of keyword-args
        :param prefix: prefix used in gcs path just after bucketname
        :param file_format: file format for local_file_path
        :param schema_defs: Schema Definitions in [(name, type, mode)] format
        :param max_bad_records: max bad records
        :param database: database to override defaults
        :param hour: timestamp of job calling the func
    :return: None
    """
    guid = log.handlers[0].baseFilename.split('/')[-1].split('__')[-1]
    max_bad_records = kwargs['max_bad_records'] if 'max_bad_records' in kwargs.keys() else 0
    hour = kwargs['hour'] if 'hour' in kwargs.keys() else None
    if dbtype == 'bigquery':
        if 'prefix' in kwargs.keys():
            gcs_path = upload_to_cloud_storage(log, config, local_file_path, prefix=kwargs['prefix'], hour=hour,
                                               projectname=project)
        else:
            gcs_path = upload_to_cloud_storage(log, config, local_file_path, hour=hour,
                                               projectname=project)

        raw_table = f'{table}_{guid}'
        file_format = kwargs['file_format'] if 'file_format' in kwargs.keys() else 'csv'
        loaded_rows, columns, loaded_to_main = load_to_table(log, config, gcs_path, raw_table, project, dataset=schema,
                                                             file_format=file_format, schema_defs=kwargs['schema_defs'],
                                                             max_bad_records=max_bad_records
                                                             )
        creds = config.dwh_creds[dbtype][project]
        pname = creds['project']

        if loaded_rows > 0 and not loaded_to_main:
            cond = []
            for pkey in pkeys:
                cond.append(f'`{pname}.{schema}.{table}`.{pkey} = `{pname}.{schema}.{table}_{guid}`.{pkey}')
            cond_str = " and ".join(cond)
            cond_str = 'TRUE' if cond_str.strip()=='' else cond_str

            columns_list_str = '`' + '`, `'.join(columns) + '`'

            upsert_script = load_sql(subfolder_path(config.dir_sql, dbtype), 'bq_load_table_generic')
            upsert_script = upsert_script.format(project=pname, dataset=schema, table=table, guid=guid,
                                                 conditions=cond_str, columns_list=columns_list_str)

            elapsed_time, _ = execute_sql(log, config, sql_query=upsert_script, db=dbtype, creds=creds)
        else:
            drop_script = load_sql(subfolder_path(config.dir_sql, dbtype), 'bq_load_table_generic_drop_only')
            drop_script = drop_script.format(dataset=schema, table=table, guid=guid)

            elapsed_time, _ = execute_sql(log, config, sql_query=drop_script, db=dbtype, creds=creds)
    elif dbtype == 'mysql':
        _df = pd.read_json(local_file_path, lines=True)
        _creds = config.dwh_creds['mysql']['s6_master']
        _creds['database'] = schema
        if _df.shape[0] > 0:
            conn = connect_to_database(log, _creds, db='mysql', raw=False,
                                       database=schema)
            _df.to_sql(f'{table}_{guid}', conn, if_exists='replace', index=False)

            cond = []
            for pkey in pkeys:
                cond.append(f'{schema}.{table}.{pkey} = {schema}.{table}_{guid}.{pkey}')
            cond_str = " and ".join(cond)

            columns_list_str = '`' + '`, `'.join(_df.columns) + '`'

            upsert_script = load_sql(subfolder_path(config.dir_sql, dbtype), 'mysql_load_table_generic')
            upsert_script = upsert_script.format(schema=schema, table=table, guid=guid,
                                                 conditions=cond_str, columns_list=columns_list_str)

            elapsed_time, _ = execute_sql(log, config, sql_query=upsert_script, db=dbtype, creds=_creds)
        else:
            drop_script = load_sql(subfolder_path(config.dir_sql, dbtype),
                                   'mysql_load_table_generic_drop_only')
            drop_script = drop_script.format(schema=schema, table=table, guid=guid)

            elapsed_time, _ = execute_sql(log, config, sql_query=drop_script, db=dbtype, creds=_creds)
    elif dbtype == 'redshift':
        # File To S3
        today = str(datetime.datetime.now().date()).replace('-', '/')
        s3_creds = config.dwh_creds[dbtype][project]

        s3_key = f"{today}/{kwargs.get('prefix', 'data')}/{local_file_path.split('/')[-1]}"
        s3_bucketpath = f'{config.s3_bucket_data}/{s3_key}'
        # log.info(f'Dumping {local_file_path} to S3 path: s3://{s3_bucketpath}')
        s3_upload_file(log, s3_creds['access_key'], s3_creds['secret_key'], config.s3_bucket_data, s3_key, local_file_path)

        tablename_raw = table + f'_{guid}'
        create_table = load_sql(subfolder_path(config.dir_sql, 'redshift/ddl'), f'{table}').format(guid='')
        create_table_raw = load_sql(subfolder_path(config.dir_sql, 'redshift/ddl'), f'{table}').format(guid=f'_{guid}')

        load_raw = load_sql(subfolder_path(config.dir_sql, dbtype),
                            's3_to_redshift_json').format(schema=schema,
                                                          table=tablename_raw,
                                                          bucketpath=s3_bucketpath,
                                                          access_key=s3_creds['access_key'],
                                                          secret_key=s3_creds['secret_key'],
                                                          )
        if pkeys is None or (isinstance(pkeys, list) and len(pkeys) == 0):
            raw_to_main = load_sql(subfolder_path(config.dir_sql, dbtype),
                                   'raw_to_main_truncate').format(schema=schema,
                                                                  table=table,
                                                                  table_raw=tablename_raw
                                                                  )
        else:
            log.info('This feature still not developed')
            sys.exit(1)
        drop_raw = load_sql(subfolder_path(config.dir_sql, dbtype),
                            'drop_table').format(schema=schema,
                                                 table=tablename_raw
                                                 )

        for query in [create_table, drop_raw, create_table_raw, load_raw, raw_to_main, drop_raw]:
            execute_sql(log, config, query, dbtype)
    else:
        log.info(f'INVALID db: {dbtype}')
        sys.exit(1)


def patch_table_simple(log, config, tablename, schema_def, projectname, dbtype='bigquery', **kwargs):
    """
    Simple patching i.e. no nested/repeated fields
    Patches a destination table with potential schema def. Adds columns. No change in column type. Doesn't drop columns.
    :param log: logger obj
    :param config: config module
    :param tablename: table name
    :param schema_def: expected schema. For bigquery expects list of schemafields.
    :param projectname: project name
    :param dbtype: database type of destination table
    :param kwargs: dynamic capture of args
        :param dataset: dataset name/schema name
    :return:
    """
    if dbtype == 'bigquery':
        new_schema_def = patch_table_simple_bq(log, config, tablename, schema_def, projectname,
                                               dataset=kwargs['dataset'])
    else:
        log.info(f'dbtype {dbtype} Not Yet Supported')
        sys.exit(1)

    return new_schema_def
