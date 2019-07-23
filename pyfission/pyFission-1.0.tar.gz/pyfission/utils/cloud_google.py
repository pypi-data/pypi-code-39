import datetime
import sys
import time
import os
import copy
from google.cloud import storage, bigquery, exceptions
from pyfission.utils.util import flatten_lists_one_level, dict_merge


def upload_to_cloud_storage(log, config, local_file_path: str, **kwargs):
    """
    Wrapper to Upload File To GCS
    :param log: logger object
    :param config: config module
    :param local_file_path: absolute path to local file to be uploaded
    :param kwargs: dynamic capture of arguments
        :param hour: YYYY/MM/DD/HH format entry for placing file in GCS for easier segmentation
        :param projectname: projectname to use (default: default)
        :param full_gcs_path: Full GS Path
    :return:
    """
    date_to_use = kwargs['hour'] if 'hour' in kwargs.keys() and kwargs['hour'] else str(datetime.datetime.now().date())
    date_slash = date_to_use[0:10].replace('-', '/')
    projectname = 'default' if 'projectname' not in kwargs.keys() else kwargs['projectname']
    default_private_key = config.dwh_creds['bigquery'][projectname]['private_key']
    default_project = config.dwh_creds['bigquery'][projectname]['project']
    default_bucket = config.dwh_creds['bigquery'][projectname]['bucket']
    default_prefix = 'data'

    private_key = default_private_key if 'private_key' not in kwargs.keys() else kwargs['private_key']
    project = default_project if 'project' not in kwargs.keys() else kwargs['project']
    bucket_name = default_bucket if 'bucket' not in kwargs.keys() else kwargs['bucket']
    prefix = default_prefix if 'prefix' not in kwargs.keys() else kwargs['prefix']

    if 'full_gcs_path' in kwargs.keys():
        gcs_path = kwargs['full_gcs_path']
        bucket_name = gcs_path[5:].split('/')[0]
        gcs_blob_name = '/'.join(gcs_path[5:].split('/')[1:])

    else:
        gcs_blob_name = f"{prefix}/{date_slash}/{local_file_path.split('/')[-1]}"
        gcs_path = f'gs://{bucket_name}/{gcs_blob_name}'

    if 'GOOGLE_APPLICATION_CREDENTIALS' not in dict(os.environ).keys():
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = private_key

    try:
        client = storage.Client(project=project).from_service_account_json(private_key)

        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(gcs_blob_name)
        blob.upload_from_filename(filename=local_file_path)

        log.info(f"Upload Successful for {local_file_path} to {gcs_path}")
        return gcs_path
    except Exception as e:
        log.info(f'Error: {e}')
        sys.exit(1)


def table_exists(client, table_reference) -> bool:
    """
    Table Existence Check
    :param client: A client to connect to the BigQuery API (google.cloud.bigquery.client.Client)
    :param table_reference: A reference to the table to look for (google.cloud.bigquery.table.TableReference)
    :return: boolean flag if table exists
    """
    try:
        client.get_table(table_reference)
        return True
    except exceptions.NotFound:
        return False


def load_to_table(log, config, gcs_path, tablename, projectname, **kwargs):
    """
    Wrapper Function to Load Data from GCS PATH to Big Query Table
    :param log: logger object
    :param config: config module
    :param gcs_path: gcs path of the file
    :param tablename: destination tablename
    :param projectname: projectname to use
    :param kwargs: dynamic capture of arguments
        :param private_key: private_key
        :param project: project
        :param dataset: dataset name / schema name
        :param file_format: csv/json
        :param schema_defs: Schema Definitions in [(name, type, mode)] format
        :param max_bad_records: max bad records
    :return: rows loaded, columns and boolean flag indicating if loaded_to_main table
    """
    guid = log.handlers[0].baseFilename.split('/')[-1].split('__')[-1]
    default_private_key = config.dwh_creds['bigquery'][projectname]['private_key']
    default_project = config.dwh_creds['bigquery'][projectname]['project']
    default_dataset = config.dwh_creds['bigquery'][projectname]['dataset']
    default_file_format = bigquery.SourceFormat.CSV

    private_key = default_private_key if 'private_key' not in kwargs.keys() else kwargs['private_key']
    project = default_project if 'project' not in kwargs.keys() else kwargs['project']
    dataset_name = default_dataset if 'dataset' not in kwargs.keys() else kwargs['dataset']

    if 'GOOGLE_APPLICATION_CREDENTIALS' not in dict(os.environ).keys():
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = private_key

    bq_client = bigquery.Client(project=project).from_service_account_json(private_key)
    dataset = bq_client.dataset(dataset_name, project=project)
    table = dataset.table(tablename)
    loaded_to_main = False
    main_table_check_columns = []
    main_table_check_schema = []

    if tablename.endswith(f'_{guid}'):
        main_table_check_name = tablename.replace(f'_{guid}', '')
        try:
            main_table_check = dataset.table(main_table_check_name)
            main_table_check_schema = bq_client.get_table(main_table_check).schema
            main_table_check_columns = [col.name for col in main_table_check_schema]
            if not table_exists(bq_client, main_table_check):
                log.info(f'Main table: {main_table_check_name} does not exist, loading to main table directly.')
                tablename = main_table_check_name
                table = dataset.table(tablename)
                loaded_to_main = True
            else:
                loaded_to_main = False
        except Exception as e1:
            log.info(f'Error: {e1}')
            log.info(f'Main table: {main_table_check_name} does not exist, loading to main table directly.')
            tablename = main_table_check_name
            table = dataset.table(tablename)
            loaded_to_main = True

    # Configure Load Job
    job_config = bigquery.LoadJobConfig()
    job_config.dry_run = False
    job_config.use_query_cache = True
    job_config.use_legacy_sql = False
    if 'schema_defs' in kwargs.keys() and isinstance(kwargs['schema_defs'], list) and len(kwargs['schema_defs']) != 0:
        job_config.autodetect = False
        job_config.schema = kwargs['schema_defs']
        log.info(f'Schema def: {job_config.schema}')
    else:
        if len(main_table_check_columns) == 0:
            job_config.autodetect = True  # if not table_exists(bq_client, table) else False
    if len(main_table_check_columns) != 0:
        job_config.autodetect = False
        job_config.schema = main_table_check_schema
    job_config.encoding = 'UTF-8'
    if 'file_format' in kwargs.keys() and kwargs['file_format'] == 'csv':  # csv
        file_format = default_file_format
        job_config.allow_quoted_newlines = True
        job_config.quote_character = '"'
        job_config.skip_leading_rows = 1
    elif 'file_format' in kwargs.keys() and kwargs['file_format'] == 'json':  # json
        file_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    else:  # csv
        file_format = default_file_format
        job_config.allow_quoted_newlines = True
        job_config.quote_character = '"'

    job_config.source_format = file_format
    # Can cause unexpected errors like dropping & recreating main table
    # job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_EMPTY

    job_config.max_bad_records = kwargs['max_bad_records']

    retries = 1
    max_retries = 3
    while retries <= max_retries:
        try:
            job = bq_client.load_table_from_uri(source_uris=gcs_path, destination=table, job_config=job_config)

            assert job.job_type == 'load'
            job.result()  # Waits for table load to complete.
            assert job.state == 'DONE'
            retries += 100_000
        except Exception as e2:
            log.info(f"Error Logged: {e2}. Retrying after some time.")
            log.info(f'Error stream: {job.errors}')
            time.sleep(60 * (max_retries - retries))

            retries += 1

    final_table = bq_client.get_table(dataset.table(tablename))
    total_rows = final_table.num_rows
    columns = [col.name for col in final_table.schema]
    log.info(f"Table {tablename} Loaded Successfully with {job.output_rows} rows. Total Rows: {total_rows}")

    return job.output_rows, columns, loaded_to_main


def patch_table_simple(log, config, tablename, schema_def, projectname, **kwargs):
    """
    Wrapper function for patching table on BQ
    :param log: logger obj
    :param config: config module
    :param tablename: name of table to be patched
    :param schema_def: expected schema in [SchemaField(name, type, mode, desc, fields), ...] format
    :param projectname: project name
    :param kwargs: dynamic capture of args
        :param private_key: private_key
        :param project: project
        :param dataset: dataset name/schema name
    :return: Update Schema Definition from Table
    """
    default_private_key = config.dwh_creds['bigquery'][projectname]['private_key']
    default_project = config.dwh_creds['bigquery'][projectname]['project']
    default_dataset = config.dwh_creds['bigquery'][projectname]['dataset']

    private_key = default_private_key if 'private_key' not in kwargs.keys() else kwargs['private_key']
    project = default_project if 'project' not in kwargs.keys() else kwargs['project']
    dataset_name = default_dataset if 'dataset' not in kwargs.keys() else kwargs['dataset']

    if 'GOOGLE_APPLICATION_CREDENTIALS' not in dict(os.environ).keys():
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = private_key

    bq_client = bigquery.Client(project=project).from_service_account_json(private_key)
    table_ref = bq_client.dataset(dataset_name, project=project).table(tablename)

    if not table_exists(bq_client, table_ref):
        log.info(f'Table {tablename} does not exist. No patching required.')
        new_schema_def = schema_def
    else:
        table = bq_client.get_table(table_ref)
        existing_schema = [schema_field for schema_field in table.schema]
        patched_schema = schema_merge(existing_schema, schema_def)

        log.info(f'Patched Table Schema:\n\t{patched_schema}')
        table.schema = patched_schema
        try:
            table = bq_client.update_table(table, ['schema'])
        except Exception as e1:
            log.info(f'Failed to patch table {tablename}. Error logged: {e1}')
            sys.exit(1)
        log.info(f'Table {tablename} patched successfully.')

        time.sleep(3)  # For letting BQ stabilize
        table_ref = bq_client.dataset(dataset_name, project=project).table(tablename)
        table = bq_client.get_table(table_ref)

        new_schema_def = [schema_field for schema_field in table.schema]

    return new_schema_def


def get_schema_definition_bq(dict_sample: dict, samples: int = -1) -> list:
    """
    Returns schema definition BQ format from dict of samples
    :param dict_sample: list of data as samples
    :param samples: if <=10, no sampling, else samples the volume of data specified
    :return: schema definition BQ format i.e. list of dicts, which might be nested upto 15 levels (not checked)
    """
    schema_def = []
    if not isinstance(dict_sample, dict):
        print(f'Expected a dict but dict_sample is of type: {type(dict_sample)}')
        sys.exit(1)
    else:
        pass

    for parent_key, value_list in dict_sample.items():
        # value_list Can be a list of values or a dictionary
        sample = [value_list] if isinstance(value_list, dict) else value_list
        _type = ''
        _mode = 'NULLABLE'  # REQUIRED not yet supported
        _desc = None  # Always NULL
        _fields = []

        # list & dict are unhashable types so they need to be in elifs before usage of set ops
        if all(isinstance(x, bool) for x in sample):
            _type = 'BOOLEAN'
        elif all(isinstance(x, int) for x in sample) and len(list(set(sample))) >= 1:
            _type = 'INTEGER'
        elif all(isinstance(x, float) for x in sample):
            _type = 'NUMERIC'
        elif all(isinstance(x, dict) for x in sample):
            _type = 'RECORD'
            if len(sample) == 1:
                merged_big_dict = sample[0]
            else:
                # This is wrong as it re-transforms list into list of lists
                merged_big_dict = {}
                for current_sample in sample:
                    merged_big_dict = dict_merge(_dct=merged_big_dict, merge_dct=current_sample, add_keys=True,
                                                 samples=samples)
            _fields = get_schema_definition_bq(merged_big_dict)
        elif all(isinstance(x, list) for x in sample):
            temp_type, temp_mode = get_datatype_from_sample_bq(flatten_lists_one_level(sample))
            _mode = 'REPEATED'
            _type = temp_type if temp_mode == 'NULLABLE' else 'STRING'  # List of lists not possible

            # Handling case for sample = list of list of dicts
            if _type == 'RECORD':
                merged_big_dict = {}
                for current_sample in flatten_lists_one_level(sample):
                    merged_big_dict = dict_merge(_dct=merged_big_dict, merge_dct=current_sample, add_keys=True,
                                                 samples=samples)
                _fields = get_schema_definition_bq(merged_big_dict)
        else:
            # int('1.0') fails but float('1') does not. Hence order is imp here. INTEGER THEN NUMERIC
            try:
                if all(isinstance(int(x), int) if '_' not in str(x) and '.' not in str(x) else False for x in sample):
                    _type = 'INTEGER'
            except:
                pass

            try:
                if _type != 'INTEGER' and all(isinstance(float(x), float) if '_' not in str(x)
                                              else False for x in sample):
                    _type = 'NUMERIC'
            except:
                pass

            if _type == '':
                _type = 'STRING'

                # Special Case for datetime
                try:
                    if all(True if datetime.datetime.strptime(x[0:19], '%Y-%m-%d %H:%M:%S') else False
                           for x in sample):
                        _type = 'DATETIME'
                except:
                    pass

                # BigQuery doesn't support T styled datetime yet.
                # try:
                #     if _type != 'DATETIME' and all(True if datetime.datetime.strptime(x[0:19],
                #                                                                       '%Y-%m-%dT%H:%M:%S') else False
                #                                    for x in sample):
                #         _type = 'DATETIME'
                # except:
                #     pass

        schema_def.append({'name': parent_key,
                           'type': _type,
                           'mode': _mode,
                           'description': _desc,
                           'fields': _fields,
                           })
    return schema_def


def get_datatype_from_sample_bq(sample: list) -> tuple:
    """
    Returns potential datatype from sample of data
    :param sample: list of data as samples
    :return: determined datatype as string
    """
    _type = ''
    _mode = 'NULLABLE'
    if all(isinstance(x, bool) for x in filter(lambda x: x is not None, sample)):
        _type = 'BOOLEAN'
    elif all(isinstance(x, int) for x in sample) and len(list(set(sample))) >= 1:
        _type = 'INTEGER'
    elif all(isinstance(x, float) for x in sample):
        _type = 'NUMERIC'
    elif all(isinstance(x, list) for x in sample):
        _type, _ = get_datatype_from_sample_bq(flatten_lists_one_level(sample))
        _mode = 'REPEATED'
    elif all(isinstance(x, dict) for x in sample):
        _type = 'RECORD'
    else:
        # int('1.0') fails but float('1') does not. Hence order is imp here. INTEGER THEN NUMERIC
        try:
            if all(isinstance(int(x), int) if '_' not in str(x) and '.' not in str(x) else False for x in sample):
                _type = 'INTEGER'
        except:
            pass

        try:
            if _type != 'INTEGER' and all(isinstance(float(x), float) if '_' not in str(x) else False for x in sample):
                _type = 'NUMERIC'
        except:
            pass

        if _type == '':
            _type = 'STRING'

            # Special Case for datetime
            try:
                if all(True if datetime.datetime.strptime(x[0:19], '%Y-%m-%d %H:%M:%S') else False
                       for x in sample):
                    _type = 'DATETIME'
            except:
                pass

            # BigQuery doesn't support T styled datetime yet.
            # try:
            #     if _type != 'DATETIME' and all(True if datetime.datetime.strptime(x[0:19],
            #                                                                       '%Y-%m-%dT%H:%M:%S') else False
            #                                    for x in sample):
            #         _type = 'DATETIME'
            # except:
            #     pass

    return _type, _mode


def get_table_schemadef(log, config, projectname, tablename, **kwargs):
    """
    Get schema def of a table in BQ
    :param log: logger obj
    :param config: config module
    :param projectname: project name
    :param tablename: table name
    :param kwargs: dynamic capture of args
        :param private_key: private_key
        :param project: project
        :param dataset: dataset
    :return: Schema def
    """
    default_private_key = config.dwh_creds['bigquery'][projectname]['private_key']
    default_project = config.dwh_creds['bigquery'][projectname]['project']
    default_dataset = config.dwh_creds['bigquery'][projectname]['dataset']

    private_key = default_private_key if 'private_key' not in kwargs.keys() else kwargs['private_key']
    project = default_project if 'project' not in kwargs.keys() else kwargs['project']
    dataset_name = default_dataset if 'dataset' not in kwargs.keys() else kwargs['dataset']

    if 'GOOGLE_APPLICATION_CREDENTIALS' not in dict(os.environ).keys():
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = private_key

    bq_client = bigquery.Client(project=project).from_service_account_json(private_key)
    table_ref = bq_client.dataset(dataset_name, project=project).table(tablename)
    table = bq_client.get_table(table_ref)

    return [schema_field for schema_field in table.schema]


def schema_merge(old_schema, new_schema):
    """
    Merges 2 Schemas to find longest schema
    :param old_schema: List of SchemaFields
    :param new_schema: List of SchemaFields
    :return: List of SchemaFields (merged)
    """
    # print(f"Old: {old_schema}", '\n\n', f"New: {new_schema}")  # Test Only
    if isinstance(old_schema, tuple):
        final_schema = copy.deepcopy(list(old_schema))
    else:
        final_schema = copy.deepcopy(old_schema)
    for sd in new_schema:
        if sd.name.lower() not in [_sd.name.lower() for _sd in final_schema]:
            final_schema.append(sd)
        else:
            old_sd = None
            old_sd_idx = None
            for idx, _sd in enumerate(final_schema):
                if _sd.name.lower() == sd.name.lower():
                    old_sd = _sd
                    old_sd_idx = idx

            if old_sd.field_type == 'RECORD':
                final_schema.pop(old_sd_idx)
                final_schema.append(bigquery.SchemaField(name=old_sd.name.lower(),
                                                         field_type=old_sd.field_type,
                                                         mode=old_sd.mode,
                                                         description=old_sd.description,
                                                         fields=schema_merge(old_sd.fields, sd.fields)))
            else:
                pass

    final_schema = sorted(final_schema, key=lambda i: i.name.lower())
    return final_schema
