import pandas as pd
import json
import itertools
import warnings
import asyncio

from .query import Query, delete_golden
from .schema_generator import carolSchemaGenerator
from .connectors import Connectors
from .storage import Storage
from .utils.importers import _import_dask, _import_pandas
from .filter import Filter, TYPE_FILTER
from .utils import async_helpers
from .utils.miscellaneous import stream_data

_SCHEMA_TYPES_MAPPING = {
    "geopoint": str,
    "long": int,
    "double": float,
    "nested": str,
    "string": str,
    "base64": str,
    "date": str,
    "boolean": bool
}



class Staging:
    def __init__(self, carol):
        self.carol = carol

    def send_data(self, staging_name, data=None, connector_name=None, connector_id=None, step_size=500,
                  print_stats=True, gzip=True, auto_create_schema=False, crosswalk_auto_create=None,
                  flexible_schema=False, force=False,  max_workers=2,  dm_to_delete=None,
                  async_send=False,
                  carol_data_storage=False):
        '''
        :param staging_name:  `str`,
            Staging name to send the data.
        :param data: pandas data frame, json. default `None`
            Data to be send to Carol
        :param connector_name: `str`, default `None`
            Connector name where the staging should be.
        :param connector_id: `str`, default `None`
            Connector Id where the staging should be.
        :param step_size: `int`, default `500`
            Number of records to be sent in each iteration. Max size for each batch is 10MB
        :param print_stats: `bool`, default `True`
            If print the status
        :param gzip: `bool`, default `True`
            If send each batch as a gzip file.
        :param auto_create_schema: `bool`, default `False`
            If to auto create the schema for the data being sent.
        :param crosswalk_auto_create: `list`, default `None`
            If `auto_create_schema=True`, crosswalk list of fields.
        :param flexible_schema: `bool`, default `False`
            If `auto_create_schema=True`, to use a flexible schema.
        :param force: `bool`, default `False`
            If `force=True` it will not check for repeated records according to crosswalk. If `False` it will check for
            duplicates and raise an error if so.
        :param max_workers: `int`, default `2`
            To be used with `async_send=True`. Number of threads to use when sending.
        :param dm_to_delete: `str`, default `None`
            Name of the data model to be erased before send the data.
        :param async_send: `bool`, default `False`
            To use async to send the data. This is much faster than a sequential send.
        :param carol_data_storage: `bool`, default `False`
            To use Carol Data Storage flow.
        :return: None
        '''

        self.gzip = gzip
        extra_headers = {}
        content_type = 'application/json'
        if self.gzip:
            content_type = None
            extra_headers["Content-Encoding"] = "gzip"
            extra_headers['content-type'] = 'application/json'

        if connector_name:
            connector_id = self._connector_by_name(connector_name)
        else:
            if connector_id is None:
                connector_id = self.carol.connector_id

        schema = self.get_schema(staging_name, connector_id=connector_id)

        is_df = False
        if isinstance(data, pd.DataFrame):
            is_df = True
            data_size = data.shape[0]
            _sample_json = data.iloc[0].to_json(date_format='iso')
        elif isinstance(data, str):
            data = json.loads(data)
            data_size = len(data)
            _sample_json = data[0]
        else:
            data_size = len(data)
            _sample_json = data[0]

        if (not isinstance(data, list)) and (not is_df):
            data = [data]
            data_size = len(data)

        if (not schema) and auto_create_schema:
            assert crosswalk_auto_create, "You should provide a crosswalk"
            self.create_schema(_sample_json, staging_name, connector_id=connector_id, export_data=carol_data_storage,
                               crosswalk_list=crosswalk_auto_create, mdm_flexible=flexible_schema)
            print('created schema...')
            _crosswalk = crosswalk_auto_create
            print('provided crosswalk ', _crosswalk)
        elif auto_create_schema:
            assert crosswalk_auto_create, "You should provide a crosswalk"
            self.create_schema(_sample_json, staging_name, connector_id=connector_id, export_data=carol_data_storage,
                               crosswalk_list=crosswalk_auto_create, overwrite=True, mdm_flexible=flexible_schema)
            _crosswalk = crosswalk_auto_create
            print('provided crosswalk ', _crosswalk)
        else:
            if schema is None:
                raise Exception(f"No schema found for `staging_name={staging_name}`. \n"
                                f"Use `auto_create_schema=True`"
                                f" to create schema automaticly ")
            _crosswalk = schema["mdmCrosswalkTemplate"]["mdmCrossreference"].values()
            _crosswalk = list(_crosswalk)[0]
            print('fetched crosswalk ', _crosswalk)

        if is_df and not force:
            assert data.duplicated(subset=_crosswalk).sum() == 0, \
                "crosswalk is not unique on data frame. set force=True to send it anyway."

        if dm_to_delete is not None:
            delete_golden(self.carol, dm_to_delete)

        url = f'v2/staging/tables/{staging_name}?carolDataStorage={carol_data_storage}&returnData=false&connectorId={connector_id}'
        
        self.cont = 0
        if async_send:
            loop = asyncio.get_event_loop()
            future = asyncio.ensure_future(async_helpers.send_data_asynchronous(carol=self.carol,
                                                                                data=data,
                                                                                step_size=step_size,
                                                                                url=url,
                                                                                extra_headers=extra_headers,
                                                                                content_type=content_type,
                                                                                max_workers=max_workers,
                                                                                compress_gzip=self.gzip))
            loop.run_until_complete(future)

        else:
            for data_json, cont in stream_data(data=data,
                                               step_size=step_size,
                                               compress_gzip=self.gzip):

                self.carol.call_api(url, data=data_json, extra_headers=extra_headers, content_type=content_type,
                                    status_forcelist=[502, 429, 502],
                                    method_whitelist=frozenset(['POST'])
                                    )
                if print_stats:
                    print('{}/{} sent'.format(cont, data_size), end='\r')

    def get_schema(self, staging_name, connector_name=None, connector_id=None):

        query_string = None
        if connector_name:
            connector_id = self._connector_by_name(connector_name)

        if connector_id:
            query_string = {"connectorId": connector_id}
        try:
            return self.carol.call_api(f'v2/staging/tables/{staging_name}/schema', method='GET',
                                       params=query_string)
        except Exception:
            return None

    def create_schema(self, fields_dict=None, staging_name=None, connector_id=None, connector_name=None,
                      mdm_flexible=False,  crosswalk_name=None, crosswalk_list=None, overwrite=False, auto_send=True,
                      export_data=False, data=None):
        """

        :param fields_dict: `json`, `list of dicts`, `pandas.DataFrame`, default `None`
            Data to create schema from. `fields_dict` will be removed in the future. Use `data`
        :param staging_name:  `str`,
            Staging name to send the data.
        :param connector_name: `str`, default `None`
            Connector name where the staging should be.
        :param connector_id: `str`, default `None`
            Connector Id where the staging should be.
        :param mdm_flexible: `bool`, default `False`
            If flexible schema.
        :param crosswalk_name: `None`, default `staging_name`
            Crosswalk name in the Schema.
        :param crosswalk_list: `list`, default `None`
            Crosswalk list of fields.
        :param overwrite: `bool`, default `False`
            Overwrite current schema
        :param auto_send: `bool`, default `True`
            Send the schema after creating.
        :param export_data: `bool`, default `False`
            Export data to CDS for this staging.
        :param data: `json`, `list of dicts`, `pandas.DataFrame`, default `None`
            Data to create schema from.
        :return:
        """

        assert staging_name is not None, 'staging_name must be set.'
        assert fields_dict is not None or data is not None, 'fields_dict or df must be set'

        if fields_dict is not None:
            warnings.warn(
                "fields_dict will be deprecated, use `data`",
                DeprecationWarning, stacklevel=3
            )
            data = fields_dict

        if connector_name:
            connector_id = self._connector_by_name(connector_name)
        else:
            assert connector_id, f'connector_id or connector name should be set.'

        if data is not None:
            if isinstance(data, pd.DataFrame):
                data = data.iloc[0].to_dict()

        if isinstance(data, list):
            data = data[0]

        if isinstance(data, dict):
            schema = carolSchemaGenerator(data)
            schema = schema.to_dict(mdmStagingType=staging_name, mdmFlexible=mdm_flexible, export_data=export_data,
                                    crosswalkname=crosswalk_name, crosswalkList=crosswalk_list)
        elif isinstance(data, str):
            schema = carolSchemaGenerator.from_json(data)
            schema = schema.to_dict(mdmStagingType=staging_name, mdmFlexible=mdm_flexible, export_data=export_data,
                                    crosswalkname=crosswalk_name, crosswalkList=crosswalk_list)
        else:
            print('Behavior for type %s not defined!' % type(data))

        if auto_send:
            self.send_schema(schema=schema, staging_name=staging_name, connector_id=connector_id, overwrite=overwrite)
        else:
            return schema

    def send_schema(self, schema, staging_name=None, connector_id=None, connector_name=None,
                    overwrite=False):

        if connector_name:
            connector_id = self._connector_by_name(connector_name)

        if staging_name is None:
            staging_name = schema.get('mdmStagingType')
            assert staging_name is not None, f"staging_name should be given or defined in the schema."

        query_string = {"connectorId": connector_id}
        if connector_id is None:
            connector_id = self.carol.connector_id
            query_string = {"connectorId": connector_id}

        has_schema = self.get_schema(staging_name, connector_id=connector_id) is not None
        if has_schema and overwrite:
            method = 'PUT'
        else:
            method = 'POST'

        resp = self.carol.call_api('v2/staging/tables/{}/schema'.format(staging_name), data=schema, method=method,
                                   params=query_string)

    def _check_crosswalk_in_data(self, schema, _sample_json):
        crosswalk = schema["mdmCrosswalkTemplate"]["mdmCrossreference"].values()
        if all(name in _sample_json for name in crosswalk):
            pass

    def _connector_by_name(self, connector_name):
        """
        Get connector id given connector name

        :param connector_name: `str`
            Connector name
        :return: `str`
            Connector Id
        """
        return Connectors(self.carol).get_by_name(connector_name)['mdmId']

    def fetch_parquet(self, staging_name, connector_id=None, connector_name=None, backend='dask',
                      merge_records=True, return_dask_graph=False, columns=None, max_hits=None,
                      return_metadata=False, callback=None):
        """

        Fetch parquet from a staging table.

        :param staging_name: `str`,
            Staging name to fetch parquet of
        :param connector_id: `str`, default `None`
            Connector id to fetch parquet of
        :param connector_name: `str`, default `None`
            Connector name to fetch parquet of
        :param backend: ['dask','pandas'], default `dask`
            if to use either dask or pandas to fetch the data
        :param merge_records: `bool`, default `True`
            This will keep only the most recent record exported. Sometimes there are updates and/or deletions and
            one should keep only the last records.
        :param return_dask_graph: `bool`, default `false`
            If to return the dask graph or the dataframe.
        :param columns: `list`, default `None`
            List of columns to fetch.
        :param max_hits: `int`, default `None`
            Number of records to get. This only should be user for tests.
        :param return_metadata: `bool`, default `False`
            To return or not the fields ['mdmId', 'mdmCounterForEntity']
        :param callback: `callable`, default `None`
            Function to be called each downloaded file.
        :return:
        """

        assert backend == 'dask' or backend == 'pandas'
        if return_dask_graph:
            assert backend == 'dask'

        if connector_name:
            connector_id = self._connector_by_name(connector_name)
        else:
            assert connector_id

        if columns:
            mapping_columns = columns
            columns = [i.replace("-", "_") for i in columns]
            columns.extend(['mdmId', 'mdmCounterForEntity', 'mdmLastUpdated'])
            mapping_columns = dict(zip([i.replace("-", "_") for i in columns], mapping_columns))
        else:
            mapping_columns = list(self.get_schema(staging_name=staging_name,
                                                   connector_id=connector_id)['mdmStagingMapping']['properties'].keys())
            columns = [i.replace("-", "_") for i in mapping_columns]
            columns.extend(['mdmId', 'mdmCounterForEntity', 'mdmLastUpdated'])
            mapping_columns = dict(zip([i.replace("-", "_") for i in columns], mapping_columns))

        # validate export
        stags = self._get_staging_export_stats()
        if not stags.get(connector_id + '_' + staging_name):
            raise Exception(f'"{staging_name}" is not set to export data, \n '
                            f'use `dm = Staging(login).export(staging_name="{staging_name}",'
                            f'connector_id="{connector_id}", sync_staging=True) to activate')

        if stags.get(connector_id + '_' + staging_name)['mdmConnectorId'] != connector_id:
            raise Exception(
                f'"Wrong connector Id {connector_id}. The connector Id associeted to this staging is  '
                f'{stags.get(staging_name)["mdmConnectorId"]}"')

        storage = Storage(self.carol)
        if backend == 'dask':

            d = _import_dask(storage=storage, connector_id=connector_id, staging_name=staging_name,
                             merge_records=merge_records, import_type='staging', return_dask_graph=return_dask_graph,
                             mapping_columns=mapping_columns,
                             columns=columns, max_hits=max_hits)

        elif backend == 'pandas':
            d = _import_pandas(storage=storage, connector_id=connector_id,
                               staging_name=staging_name, import_type='staging',  columns=columns,
                               max_hits=max_hits, callback=callback, mapping_columns=mapping_columns)

            # TODO: Do the same for dask backend
            if d is None:
                warnings.warn(f'No data to fetch! {staging_name} has no data', UserWarning)
                cols_keys = list(self.get_schema(
                    staging_name=staging_name, connector_id=connector_id
                )['mdmStagingMapping']['properties'].keys())
                cols_keys = [i.replace("-", "_") for i in cols_keys]

                if return_metadata:
                    cols_keys.extend(['mdmId', 'mdmCounterForEntity', 'mdmLastUpdated'])

                elif columns:
                    columns = [i for i in columns if i not in ['mdmId', 'mdmCounterForEntity', 'mdmLastUpdated']]

                d = pd.DataFrame(columns=cols_keys)
                for key, value in self.get_schema(staging_name=staging_name,
                                                  connector_id=connector_id)['mdmStagingMapping'][
                    'properties'].items():
                    key = key.replace("-", "_")
                    d.loc[:, key] = d.loc[:, key].astype(_SCHEMA_TYPES_MAPPING.get(value['type'], str), copy=False)
                if columns:
                    columns = list(set(columns))
                    d = d[list(set(columns))]
                return d.rename(columns=mapping_columns)
        else:
            raise ValueError(f'backend should be either "dask" or "pandas" you entered {backend}')

        if merge_records:
            if not return_dask_graph:
                d.sort_values('mdmCounterForEntity', inplace=True)
                d.reset_index(inplace=True, drop=True)
                d.drop_duplicates(subset='mdmId', keep='last', inplace=True)
                d.reset_index(inplace=True, drop=True)
            else:
                d = d.set_index('mdmCounterForEntity', sorted=True) \
                    .drop_duplicates(subset='mdmId', keep='last') \
                    .reset_index(drop=True)

        if not return_metadata:
            to_drop = set(['mdmId', 'mdmCounterForEntity', 'mdmLastUpdated']).intersection(set(d.columns))
            d = d.drop(labels=to_drop, axis=1)

        return d

    def export(self, staging_name, connector_id=None, connector_name=None, sync_staging=True, full_export=False,
               delete_previous=False):
        """

        Export Staging to s3

        This method will trigger or pause the export of the data in the staging to
        s3.

        :param staging_name: `str`, default `None`
            Staging Name
        :param sync_staging: `bool`, default `True`
            Sync the data model
        :param connector_name: `str`
            Connector name
        :param connector_id: `str`
            Connector id
        :param full_export: `bool`, default `True`
            Do a resync of the data model
        :param delete_previous: `bool`, default `False`
            Delete previous exported files.
        :return: None


        Usage:
        To trigger the export the first time:

        >>>from pycarol.staging import Staging
        >>>from pycarol.auth.PwdAuth import PwdAuth
        >>>from pycarol.carol import Carol
        >>>login = Carol()
        >>>stag  = Staging(login)
        >>>stag.export(staging, connector_name=connector_name,sync_staging=True)

        To do a resync, that is, start the sync from the begining without delete old data
        >>>stag.export(staging, connector_name=connector_name,sync_staging=True, full_export=True)

        To delete the old data:
        >>>stag.export(staging, connector_name=connector_name,sync_staging=True, full_export=True, delete_previous=True)

        To Pause a sync:
        >>>stag.export(staging, connector_name=connector_name,sync_staging=False)
        """

        if sync_staging:
            status = 'RUNNING'
        else:
            status = 'PAUSED'

        if connector_name:
            connector_id = self._connector_by_name(connector_name)
        else:
            assert connector_id

        query_params = {"status": status, "fullExport": full_export,
                        "deletePrevious": delete_previous}
        url = f'v2/staging/{connector_id}/{staging_name}/exporter'
        return self.carol.call_api(url, method='POST', params=query_params)

    def export_all(self, connector_id=None, connector_name=None, sync_staging=True, full_export=False,
                   delete_previous=False):
        """

        Export all Stagings from a connector to s3

        This method will trigger or pause the export of all stagings  to
        s3.

        :param sync_staging: `bool`, default `True`
            Sync the data model
        :param connector_name: `str`
            Connector name
        :param connector_id: `str`
            Connector id
        :param full_export: `bool`, default `True`
            Do a resync of the data model
        :param delete_previous: `bool`, default `False`
            Delete previous exported files.
        :return: None

        Usage: See `Staging.export()`
        """
        if connector_name:
            connector_id = self._connector_by_name(connector_name)
        else:
            assert connector_id

        conn_stats = Connectors(self.carol).stats(connector_id=connector_id)

        for staging in conn_stats.get(connector_id):
            self.export(staging_name=staging, connector_id=connector_id,
                        sync_staging=sync_staging, full_export=full_export, delete_previous=delete_previous)

    def _get_staging_export_stats(self):
        """
        Get export status for data models

        :return: `dict`
            dict with the information of which staging table is exporting its data.
        """

        query = Query(self.carol, index_type='CONFIG', only_hits=False)

        json_q = Filter.Builder(key_prefix="") \
            .must(TYPE_FILTER(value="mdmStagingDataExport")).build().to_json()

        query.query(json_q, ).go()
        staging_results = query.results
        staging_results = [elem.get('hits', elem) for elem in staging_results
                           if elem.get('hits', None)]
        staging_results = list(itertools.chain(*staging_results))
        if staging_results is not None:
            return {f"{i.get('mdmConnectorId', 'connectorId_not_found')}_{i.get('mdmStagingType', 'staging_not_found')}": i for i in staging_results}

    def _sync_counters(self, staging_name, connector_id=None, connector_name=None, incremental=False):
        """

        :param staging_name: `str`
            Staging Name
        :param connector_name: `str`, default `None`
            Connector name
        :param connector_id: `str`, default `None`
            Connector id
        :param incremental: `bool`, default `False`
            If `True`, it will reset all `mdmCountForEntity`, if `False`, it will only increment the missing values.

        :return: None
        """

        if connector_name:
            connector_id = self._connector_by_name(connector_name)
        else:
            assert connector_id

        query_params = {"incrementAll": incremental}
        url = f'v2/staging/{connector_id}/{staging_name}/syncCounters'
        return self.carol.call_api(url, method='POST', params=query_params, errors='ignore')

    def get_mapping_snapshot(self, connector_id, mapping_id, entity_space='PRODUCTION', reverse_mapping=False):

        self.snap = {}
        querystring = {"entitySpace": entity_space, "reverseMapping": reverse_mapping}

        url = f"v1/connectors/{connector_id}/entityMappings/{mapping_id}/snapshot"
        response = self.carol.call_api(url, method='GET', params=querystring, )

        mapping_name = response.get('entityMappingName')
        return {mapping_name: response}

    def delete_mapping(self, staging_name=None, connector_id=None, connector_name=None, mapping_id=None,
                       entity_space='PRODUCTION'):

        cc = Connectors(self.carol)
        st = cc.get_dm_mappings(all_connectors=True)

        if mapping_id is None:
            assert staging_name is not None, "staging_name should be set."
            if (connector_id is None) and (connector_name is not None):
                connector_id = Connectors(self.carol).get_by_name(connector_name)['mdmId']
                entity = [i['mdmId'] for i in st
                          if (i.get('mdmConnectorId') == connector_id) and
                          (i.get('mdmStagingType') == staging_name)]
                assert len(entity) == 1, f'No data model mapped for {staging_name}'
                mapping_id = entity[0]

            elif connector_id is None:
                entity = [i for i in st if (i.get('mdmStagingType') == staging_name)]

                if len(entity) > 1:
                    raise KeyError(f'There are more than one connector for staging {staging_name}')
                elif len(entity) < 1:
                    raise KeyError(f'No data model mapped for {staging_name}')
                entity = entity[0]
                connector_id = entity['mdmConnectorId']
                mapping_id = entity['mdmId']
            elif connector_id:
                entity = [i['mdmId'] for i in st
                          if (i.get('mdmConnectorId') == connector_id) and
                          (i.get('mdmStagingType') == staging_name)]

                assert len(entity) == 1, f'No mapping for {staging_name}'
                mapping_id = entity[0]

        url_mapping = f'v1/connectors/{connector_id}/entityMappings/{mapping_id}'
        querystring = {"entitySpace": entity_space, "reverseMapping": "false"}

        self.carol.call_api(url_mapping, method='DELETE', params=querystring, )

    def _check_if_exists(self, connector_id, staging_name):
        conn = Connectors(self.carol)

        try:
            mappings = conn.get_dm_mappings(connector_id=connector_id, staging_name=staging_name)
            return mappings
        except Exception as e:
            if 'Entity mapping not found' in str(e):
                return None
            else:
                raise e

    def mapping_from_snapshot(self, mapping_snapshot, connector_id=None, connector_name=None,
                              publish=True, overwrite=False):

        if connector_name:
            connector_id = self._connector_by_name(connector_name)
        else:
            assert connector_id

        staging_name = mapping_snapshot.get('stagingEntityType')
        assert staging_name, f"Snapshot incomplete, `stagingEntityType` not in snapshot"

        _mappings = self._check_if_exists(connector_id=connector_id, staging_name=staging_name)

        if (_mappings is not None) and overwrite:
            _mapping_id = [i['mdmId'] for i in _mappings]
            assert len(_mapping_id) == 1
            _mapping_id = _mapping_id[0]
            method = 'PUT'
            url_mapping = f"v1/connectors/{connector_id}/entityMappings/{_mapping_id}/snapshot"
        else:
            method = 'POST'
            url_mapping = f'v1/connectors/{connector_id}/entityMappings/snapshot'

        resp = self.carol.call_api(url_mapping, method=method, data=mapping_snapshot)
        _mapping_id = resp['mdmEntityMapping']['mdmId']

        if publish:
            url = f"v1/connectors/{connector_id}/entityMappings/{_mapping_id}/publish"
            self.carol.call_api(url, method='POST')
