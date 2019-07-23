import contextlib
import datetime
import json
import os
import sys
from os.path import join
import pandas as pd
import csv
import copy
import time
from google.cloud import bigquery

from pyfission.custom_logging.__main__ import func_logger, logger_config
from pyfission.configs.fission import fission_src, fission_dest
from pyfission.utils.cloud_google import get_table_schemadef
from pyfission.utils.database import get_query_results, local_file_to_dwh, execute_sql, patch_table_simple
from pyfission.utils.worker import bash_multi_ops
from pyfission.utils.util import list_to_quoted_delimited, dump_json_list_to_ndjson


def pyfission_dump_results(log, config, src, dbtype_src, src_schema, out_format, local_file_path, query, use_method,
                           _table, src_db):
    with contextlib.suppress(FileNotFoundError):
        os.remove(local_file_path)

    timestampnow = datetime.datetime.now().strftime(config.timestamp_now_formatting)

    s_s, s_t = _table.split('.')
    tableinfo = [_tableinfo for tablename, _tableinfo in fission_src[src][src_schema].items() if tablename == s_t][0]
    pks = tableinfo['pk']
    pks_str = ', '.join(pks)

    _query = copy.deepcopy(query)
    total_chunks = 1
    schema_defs = []
    if use_method in ['full', 'incremental']:
        _, _temp_df = get_query_results(log, config, f"select count(*) as count from ({_query}) t1;", out_format='df',
                                        display_sample=False, dbtype=dbtype_src, project=src, database=src_db)
        row_count = int(_temp_df[0]['count'][0])
        total_chunks = int(row_count / config.chunksize) + 1

        if dbtype_src in ['mysql']:
            _, _temp_df = get_query_results(log, config, f"DESCRIBE {_table};", out_format='df',
                                            display_sample=False, dbtype=dbtype_src, project=src, database=src_db)
            for idx, row in _temp_df[0].iterrows():
                _type_orig = str(row['Type']).lower().split('(')[0]
                _type = config.mysql_to_bigquery[_type_orig]
                schema_defs.append((row['Field'], _type))
        elif dbtype_src in ['redshift', 'postgres']:
            desc_query = 'SELECT distinct column_name, data_type FROM information_schema.columns'
            desc_query += f" WHERE table_schema = '{s_s}' AND table_name = '{s_t}';"
            _, _temp_df = get_query_results(log, config, desc_query, out_format='df',
                                            display_sample=False, dbtype=dbtype_src, project=src, database=src_db)
            for idx, row in _temp_df[0].iterrows():
                _type_orig = str(row['data_type']).lower()
                _type = config.rs_to_bigquery[_type_orig]
                schema_defs.append((row['column_name'], _type))
        elif dbtype_src in ['mssql']:
            _, _temp_df = get_query_results(log, config, f"exec sp_columns {s_t};", out_format='df',
                                            display_sample=False, dbtype=dbtype_src, project=src, database=src_db)
            for idx, row in _temp_df[0].iterrows():
                _type_orig = str(row['TYPE_NAME']).lower().split('(')[0]
                _type = config.mssql_to_bigquery[_type_orig]
                schema_defs.append((row['COLUMN_NAME'], _type))
        elif dbtype_src in ['bigquery']:
            _schema_def = get_table_schemadef(log, config, src, s_t, dataset=s_s)
            for _sd in _schema_def:
                _sd_dict = bigquery.schema.SchemaField.to_api_repr(_sd)
                schema_defs.append((_sd_dict['name'], _sd_dict['type']))
        else:
            log.info(f'Unsupported dbtype_src: {dbtype_src}')
            sys.exit(1)
        if 'bi_work_instance_id' not in [_schema_defs[0] for _schema_defs in schema_defs]:
            schema_defs.append(('bi_work_instance_id', 'datetime'))
    else:
        log.info(f'INVALID use_method {use_method}')

    if use_method in ['incremental']:
        total_chunks = min(50, total_chunks)
    # total_chunks = min(5, total_chunks)
    for i in range(total_chunks):
        log.info(f'Processing chunk {i + 1}/{total_chunks}')
        if dbtype_src in ['mssql']:
            if config.dwh_creds['mssql'][src].get('version', 2012) == 2012:
                query = _query + f" ORDER BY {pks_str} OFFSET {config.chunksize} ROWS FETCH NEXT {config.chunksize} ROWS ONLY ;"
            elif config.dwh_creds['mssql'][src].get('version', 2012) == 2008:
                _all_cols = ", ".join([schemadef[0] for schemadef in schema_defs
                                       if schemadef[0] != 'bi_work_instance_id'])
                query = f"select {_all_cols} from (select {_all_cols}, ROW_NUMBER() OVER (ORDER BY {_all_cols}) AS seqbiseq from {_table}) t "
                query += f"WHERE seqbiseq BETWEEN {i * config.chunksize} AND {(i + 1) * config.chunksize - 1}"
            else:
                log.info('Invalid SQL Server version.')
                sys.exit(1)
        else:
            query = _query + f" ORDER BY {pks_str} LIMIT {config.chunksize} OFFSET {i * config.chunksize} ;"

        use_out_format = 'df' if dbtype_src in ['bigquery'] else 'list'
        _, _op = get_query_results(log, config, query, out_format=use_out_format, display_sample=False,
                                   dbtype=dbtype_src, project=src, database=src_db)
        data = _op[0]
        cols = _op[1]

        if isinstance(data, list):
            if 'bi_work_instance_id' not in cols:
                cols.append('bi_work_instance_id')
            if out_format == 'csv':
                with open(local_file_path, 'a', encoding='utf-8') as f_out:
                    c = csv.writer(f_out, delimiter=',', quoting=csv.QUOTE_ALL, escapechar='\\')
                    if i < 1:  # Write header only first iteration
                        c.writerow(cols)
                    for row_as_list in data:
                        if 'bi_work_instance_id' in cols:
                            c.writerow(row_as_list.append(timestampnow))
                        else:
                            c.writerow(row_as_list)
            elif out_format == 'json':
                with open(local_file_path, 'a', encoding='utf-8') as f_out:

                    for row_as_list in data:
                        if isinstance(row_as_list, dict):
                            _json_data = row_as_list
                            _json_data['bi_work_instance_id'] = timestampnow
                        else:
                            _json_data = {}
                            for idx, col in enumerate(cols):
                                if col == 'bi_work_instance_id':
                                    _json_data[col] = timestampnow
                                else:
                                    _json_data[col] = row_as_list[idx]
                        # json.dump(clean_dictionary(_json_data, bq_fix=True), f_out) # To avoid column mismatch
                        json.dump(_json_data, f_out)
                        f_out.write('\n')
            else:
                log.info(f'INVALID out_format: {out_format}')
                sys.exit(1)
        elif isinstance(data, pd.DataFrame):
            data['bi_work_instance_id'] = timestampnow
            if out_format == 'csv':
                log.info(f'INVALID out_format: {out_format}')
                sys.exit(1)
            elif out_format == 'json':
                data_list = data.to_dict(orient='records')
                dump_json_list_to_ndjson(log, data_list, local_file_path, bq_fix=False, already_flat=True)
            else:
                log.info(f'INVALID out_format: {out_format}')
                sys.exit(1)
        else:
            log.info(f'INVALID datatype for variable data: {type(data)}')
            sys.exit(1)

    return schema_defs


@func_logger(ignore_args=[], ignore_kwargs=[])
def pyfission(log, config, args):
    data = pd.DataFrame()
    guid = log.handlers[0].baseFilename.split('/')[-1].split('__')[-1]
    src = args.src
    dest = args.dest
    db = args.src_schema
    src_table = args.src_table
    src_db = None if str(args.src_db).lower() == 'none' else args.src_db
    dest_db = None if str(args.dest_db).lower() == 'none' else args.dest_db
    f_out = join(config.dir_storage, f'{guid}_{db}_{src_table}')
    _table = f'{db}.{src_table}'

    dbtype_src = [_key for _key, _value in config.dwh_creds.items() for __key, __value in _value.items()
                  if __key == src][0]
    dbtype_dest = [_key for _key, _value in config.dwh_creds.items() for __key, __value in _value.items()
                   if __key == dest][0]
    tableinfo = [_tableinfo for tablename, _tableinfo in fission_src[src][db].items() if tablename == src_table][0]
    dest_schema = fission_dest[dest][src]
    pks = tableinfo['pk']
    pks_skip = tableinfo.get('skip_max_pk_check', [])
    rks = tableinfo['rk']

    if not args.method:
        use_method = tableinfo['method'] if 'method' in tableinfo.keys() else 'full'
    else:
        use_method = args.method

    query = f"select * from {db}.{src_table}"
    if use_method == 'full':
        pass
    elif use_method == 'incremental':
        where_cond = []

        # Conditions by rk
        lookback = str(datetime.datetime.now() - datetime.timedelta(days=1))[0:10]
        for rk in rks:
            where_cond.append(f"{rk} >= '{lookback}'")

        # Conditions by pk
        new_pks = list(set(pks) - set(pks_skip))
        pk_maxes = ','.join([f'coalesce(max({pk}), 0) as max_{pk}' for pk in new_pks])
        _max_pk_query = f'select {pk_maxes} from {dest_schema}.{src_table};'
        retry = 0

        try:
            while retry < 5:
                try:
                    _, _op = get_query_results(log, config, _max_pk_query, out_format='df', display_sample=False,
                                               dbtype=dbtype_dest, project=dest, database=src_db)
                    data = _op[0]
                    retry = 100
                except:
                    time.sleep(10)
                    retry += 1
                    data = []
            if not isinstance(data, pd.DataFrame):
                data = [0] * len(new_pks)
        except:
            data = [0] * len(new_pks)

        for pk in new_pks:
            if isinstance(data, list):
                pk_max_val = 0
            else:
                pk_max_val = data[f'max_{pk}'].tolist()[0]
            if isinstance(pk_max_val, int) or isinstance(pk_max_val, float):
                where_cond.append(f"{pk} >= {pk_max_val}")
            else:
                where_cond.append(f"{pk} >= '{pk_max_val}'")

        where_conditon = " or ".join(where_cond)
        query += f" where {where_conditon} "
    else:
        log.info(f"INVALID method {use_method}")
        sys.exit(1)

    try:
        schema_defs = pyfission_dump_results(log, config, src, dbtype_src, args.src_schema, args.out_format, f_out,
                                             query,
                                             use_method, _table=_table, src_db=src_db)
        if dbtype_dest == 'bigquery':
            schema_defs = [bigquery.SchemaField(sd[0], sd[1]) for sd in schema_defs]
            new_schema_def = patch_table_simple(log, config, src_table, schema_defs, projectname=args.dest,
                                                dbtype=dbtype_dest, dataset=dest_schema)
        elif dbtype_dest == 'mysql':
            new_schema_def = None
        else:
            log.info(f'Unsupported dbtype_dest = {dbtype_dest}')
            sys.exit(1)
        local_file_to_dwh(log, config, f_out, dbtype_dest, dest, dest_schema, src_table, pks, prefix='fission',
                          file_format=args.out_format, schema_defs=new_schema_def)
    except Exception as e1:
        log.info(f"Error Logged: {e1}. Args: {args}")
        sys.exit(1)

    ub = 16  # 16 = 04:00 PM
    lb = 11  # 11 = 11:00 AM
    time_check = True if int(datetime.datetime.now().time().strftime('%H')) in list(range(lb, ub, 3)) else False
    skip_check = tableinfo.get('skip_integrity_check', False)
    time_check = time_check if tableinfo.get('skip_integrity_check', False) else True
    if (not skip_check) or time_check:
        pk_switcher = {'redshift': "||'-'||".join([f"CAST({pk} AS VARCHAR)" for pk in pks]),
                       'postgres': "||'-'||".join([f"CAST({pk} AS VARCHAR)" for pk in pks]),
                       'mysql': "concat(" + ",'-',".join([f"CAST({pk} AS CHAR)" for pk in pks]) + ")",
                       'bigquery': "concat(" + ",'-',".join([f"CAST({pk} AS STRING)" for pk in pks]) + ")",
                       'mssql': " " + "+'-'+".join(pks) + " ",
                       }
        pk_find_query_src = f'SELECT {pk_switcher[dbtype_src]} as pkids from {db}.{src_table};'
        pk_find_query_dest = f'SELECT {pk_switcher[dbtype_dest]} as pkids from {dest_schema}.{src_table};'

        _, _op_src = get_query_results(log, config, pk_find_query_src, out_format='df', display_sample=False,
                                       dbtype=dbtype_src, project=src, database=src_db)
        _, _op_dest = get_query_results(log, config, pk_find_query_dest, out_format='df', display_sample=False,
                                        dbtype=dbtype_dest, project=dest, database=dest_db)

        src_pkids = _op_src[0]['pkids'].tolist()
        dest_pkids = _op_dest[0]['pkids'].tolist()
        to_insert = list(set(src_pkids) - set(dest_pkids))[0:25000]

        # Inserting
        if len(to_insert) > 0:
            log.info(f'These pkids (first 1000) needs to be inserted:\n{to_insert[:1000]}')
            to_insert_str = list_to_quoted_delimited(to_insert, delimiter=',')
            find_inserts = f"select * from {db}.{src_table} where {pk_switcher[dbtype_src]} in ({to_insert_str})"

            try:
                schema_defs = pyfission_dump_results(log, config, src, dbtype_src, args.src_schema, args.out_format,
                                                     f_out, find_inserts, use_method, _table=_table, src_db=src_db)
                if dbtype_dest == 'bigquery':
                    schema_defs = [bigquery.SchemaField(sd[0], sd[1]) for sd in schema_defs]
                    new_schema_def = patch_table_simple(log, config, src_table, schema_defs, projectname=args.dest,
                                                        dbtype=dbtype_dest, dataset=dest_schema)
                elif dbtype_dest == 'mysql':
                    new_schema_def = None
                else:
                    log.info(f'Unsupported dbtype_dest = {dbtype_dest}')
                    sys.exit(1)
                local_file_to_dwh(log, config, f_out, dbtype_dest, dest, dest_schema, src_table, pks, prefix='fission',
                                  file_format=args.out_format, schema_defs=new_schema_def)
            except Exception as e2:
                log.info(f"Error Logged: {e2}. Args: {args}")
                sys.exit(1)

            # Refresh the pkids on dest to find stuff that needs deletion
            _, _op_dest = get_query_results(log, config, pk_find_query_dest, out_format='df', display_sample=False,
                                            dbtype=dbtype_dest, project=dest, database=dest_db)
        else:
            log.info(f'Nothing to insert to {dest_schema}.{src_table}')

        dest_pkids = _op_dest[0]['pkids'].tolist()
        to_del = list(set(dest_pkids) - set(src_pkids))

        # Deleting
        if len(to_del) > 0:
            log.info(f'Deleting from {dest_schema}.{src_table} | {len(to_del)} ids: {to_del}')
            to_del_pkeylist = ', '.join("'{0}'".format(k) for k in to_del[:1000])
            del_sql = f"delete from {dest_schema}.{src_table} where {pk_switcher[dbtype_dest]} in ({to_del_pkeylist});"

            creds = config.dwh_creds[dbtype_dest][dest]
            elapsed_time, _ = execute_sql(log, config, sql_query=del_sql, db=dbtype_dest, creds=creds)
        else:
            log.info(f'Nothing to delete from {dest_schema}.{src_table}')

    return None


def pyfission_orch(guid, config, args):
    """
    Orchestration function for pyfission. For no inputs, the default action is to run all.
    :param log: logger object
    :param config: config module
    :param args: args
    :return: None
    """
    log = logger_config(guid=guid, prefix=f'{str(__name__).replace(".", "__")}')
    src = args.src
    dest = args.dest
    src_db = args.src_db
    dest_db = args.dest_db

    if not args.src_table and not args.src_schema:
        all_bash_cmd = []
        for db, tables in fission_src[src].items():
            log.info(f'Processing: {len(tables.keys())} tables for sync in parallel')
            for tablename, tableinfo in tables.items():
                if not args.method:
                    use_method = tableinfo['method'] if 'method' in tableinfo.keys() else 'full'
                else:
                    use_method = args.method

                general_cmd = f"{config.python_exec} -m pyfission --src {src} --dest {dest} sync --method {use_method}"
                final_cmd = f"{general_cmd} --src_table {tablename} --src_schema {db}"
                if src_db is not None:
                    final_cmd += f' --src_db {src_db}'
                if dest_db is not None:
                    final_cmd += f' --dest_db {dest_db}'

                if args.out_format:
                    all_bash_cmd.append(f"{final_cmd} --out_format {args.out_format}")
                else:
                    all_bash_cmd.append(f"{final_cmd} --out_format csv")

        elapsed_time, _ = bash_multi_ops(log, config, all_bash_cmd, chunk_size=10)

    else:
        module_name = str(__name__).replace('.', '__')
        log = logger_config(guid=guid, prefix=f'{module_name}__{args.src_table}')
        elapsed_time, _ = pyfission(log, config, args)

    log.info(f'Total Time Elapsed: {elapsed_time.total_seconds()}')
