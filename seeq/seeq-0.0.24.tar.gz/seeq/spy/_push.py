import datetime
import json
import re
import six
import time

import pandas as pd
import numpy as np

from seeq.base import gconfig
from seeq.sdk import *
from seeq.sdk.rest import ApiException

from . import _common
from . import _login
from .assets import Model


def push(data=None, metadata=None, item_type=None, workbook=_common.DEFAULT_WORKBOOK_PATH,
         worksheet='From Data Lab', datasource=None, archive=False, type_mismatches='raise', errors='catalog'):
    workbooks_api = WorkbooksApi(_login.client)
    signals_api = SignalsApi(_login.client)
    conditions_api = ConditionsApi(_login.client)
    datasources_api = DatasourcesApi(_login.client)

    if data is not None:
        if isinstance(data, Model):
            metadata = data.to_dataframe()
            data = None
        elif not isinstance(data, pd.DataFrame):
            raise Exception('"data" must be a DataFrame or Model')

    if metadata is not None:
        if isinstance(metadata, Model):
            metadata = data.to_dataframe()
        elif not isinstance(metadata, pd.DataFrame):
            raise Exception('"metadata" must be a DataFrame or Model')

    datasource_input = DatasourceInputV1()
    if datasource is not None:
        if not isinstance(datasource, dict):
            raise Exception('"datasource" parameter must be dict')

        if 'Datasource Class' not in datasource:
            raise Exception('"Datasource Class" required for datasource. This is the type of data being pushed. '
                            'For example, "WITSML"')

        if 'Datasource Name' not in datasource:
            raise Exception('"Datasource Name" required for datasource. This is the specific data set being pushed. '
                            'For example, "Permian Basin Well Data"')

        _dict_to_datasource_input(datasource, datasource_input)

        if datasource_input.datasource_id is None:
            datasource_input.datasource_id = datasource_input.name

    else:
        datasource_input.name = _common.DEFAULT_DATASOURCE_CLASS
        datasource_input.description = 'Signals, conditions and scalars from Seeq Data Lab.'
        datasource_input.datasource_class = _common.DEFAULT_DATASOURCE_CLASS
        datasource_input.datasource_id = _common.DEFAULT_DATASOURCE_ID

    datasource_input.stored_in_seeq = True
    datasource_output = datasources_api.create_datasource(body=datasource_input)  # type: DatasourceOutputV1

    workbook_id = None
    workstep_json = None
    if workbook is not None:
        workbook_id = reify_workbook(workbook)

        worksheets_output = workbooks_api.get_worksheets(workbook_id=workbook_id,
                                                         limit=10000)  # type: WorksheetOutputListV1

        existing_worksheet = None
        for worksheet_output in worksheets_output.worksheets:  # type: WorksheetOutputV1
            if worksheet_output.name == worksheet:
                existing_worksheet = worksheet_output
                break

        if not existing_worksheet:
            worksheet_input = WorksheetInputV1()
            worksheet_input.name = worksheet
            existing_worksheet = workbooks_api.create_worksheet(workbook_id=workbook_id,
                                                                body=worksheet_input)  # type: WorksheetOutputV1

        worksheet_id = existing_worksheet.id

        workstep_input = WorkstepInputV1()
        if existing_worksheet.workstep:
            workstep_id = existing_worksheet.workstep.split('/')[-1]
            workstep_output = workbooks_api.get_workstep(workbook_id=workbook_id,
                                                         worksheet_id=worksheet_id,
                                                         workstep_id=workstep_id)  # type: WorkstepOutputV1
            workstep_input.data = workstep_output.data

        if workstep_input.data:
            workstep_json = json.loads(workstep_input.data)

        _now = int(round(time.time() * 1000))
        if not workstep_json:
            workstep_json = {
                "version": 24,
                "state": {
                    "stores": {
                        "sqTrendSeriesStore": {
                            "items": [
                            ]
                        },
                        "sqDurationStore": {
                            "autoUpdate": {
                                "mode": "OFF",
                                "offset": 0,
                                "manualInterval": {
                                    "value": 1,
                                    "units": "min"
                                }
                            },
                            "displayRange": {
                                "start": _now - (24 * 60 * 60 * 1000),
                                "end": _now
                            },
                            "investigateRange": {
                                "start": _now - (24 * 60 * 60 * 1000),
                                "end": _now
                            }
                        }
                    }
                }
            }

    push_result_df = pd.DataFrame()
    if metadata is not None:
        if data is None:
            push_result_df = _push_metadata(metadata, workbook_id, datasource_output, archive, errors)
        else:
            push_result_df = metadata.copy()

    if data is not None:
        earliest_sample = None
        latest_sample = None

        def _put_item_defaults(d):
            if 'Datasource Class' not in d:
                d['Datasource Class'] = _common.DEFAULT_DATASOURCE_CLASS

            if 'Datasource ID' not in d:
                d['Datasource ID'] = _common.DEFAULT_DATASOURCE_ID

            if 'Data ID' not in d:
                d['Data ID'] = d['Name']
                if workbook_id:
                    d['Data ID'] = ('[%s] ' % workbook_id) + d['Data ID']

            if workbook_id:
                d['Scoped To'] = workbook_id

        if item_type in [None, 'Signal']:
            for column in data:
                try:
                    signal_metadata = metadata.loc[column].to_dict() \
                        if metadata is not None and column in metadata.index else dict()

                    if 'Name' not in signal_metadata:
                        signal_metadata['Name'] = column

                    _put_item_defaults(signal_metadata)

                    earliest_sample, latest_sample, signal_id = _push_signal(column, signal_metadata, data,
                                                                             earliest_sample,
                                                                             latest_sample, signals_api,
                                                                             workstep_json,
                                                                             type_mismatches)
                    push_result_df.at[column, 'Push Result'] = 'Success'
                    push_result_df.at[column, 'ID'] = signal_id
                    push_result_df.at[column, 'Type'] = 'StoredSignal'

                except Exception as e:
                    if errors == 'raise':
                        raise

                    push_result_df.at[column, 'Push Result'] = e

        elif item_type == 'Condition':
            try:
                if metadata is None or len(metadata) != 1:
                    raise Exception('Condition requires "metadata" input of DataFrame with single row')

                condition_metadata = metadata.iloc[0].to_dict()

                if 'Name' not in condition_metadata or 'Maximum Duration' not in condition_metadata:
                    raise Exception('Condition metadata requires "Name" and "Maximum Duration" columns')

                if 'Capsule Start' not in data or 'Capsule End' not in data:
                    raise Exception('Condition data requires "Capsule Start" and "Capsule End" columns')

                _put_item_defaults(condition_metadata)
                earliest_sample, latest_sample, condition_id = _push_condition(condition_metadata, conditions_api, data,
                                                                               earliest_sample, latest_sample)
                push_result_df.at[0, 'Push Result'] = 'Success'
                push_result_df.at[0, 'ID'] = condition_id
                push_result_df.at[0, 'Type'] = 'StoredCondition'

            except Exception as e:
                if errors == 'raise':
                    raise

                push_result_df.at[0, 'Push Result'] = e

        if workbook_id and earliest_sample is not None and latest_sample is not None:
            workstep_json['state']['stores']['sqDurationStore']['displayRange']['start'] = earliest_sample
            workstep_json['state']['stores']['sqDurationStore']['displayRange']['end'] = latest_sample
            workstep_json['state']['stores']['sqDurationStore']['investigateRange']['start'] = earliest_sample
            workstep_json['state']['stores']['sqDurationStore']['investigateRange']['end'] = latest_sample

    if workbook_id:
        workstep_input.data = json.dumps(workstep_json)

        workstep_output = workbooks_api.create_workstep(workbook_id=workbook_id,
                                                        worksheet_id=worksheet_id,
                                                        body=workstep_input)  # type: WorkstepOutputV1

        workbooks_api.set_current_workstep(workbook_id=workbook_id,
                                           worksheet_id=worksheet_id,
                                           workstep_id=workstep_output.id)

        url = '%s/%s/workbook/%s/worksheet/%s' % (gconfig.get_api_url().replace('/api', ''),
                                                  workstep_output.id,
                                                  workbook_id,
                                                  worksheet_id)

        print('Click the following link to see your pushed data in Seeq:')
        print(url)

    return push_result_df


def _push_metadata(metadata, workbook_id, datasource_output, archive, errors):
    items_api = ItemsApi(_login.client)
    trees_api = TreesApi(_login.client)
    signals_api = SignalsApi(_login.client)
    datasources_api = DatasourcesApi(_login.client)

    metadata_df = metadata  # type: pd.DataFrame

    sync_token = datetime.datetime.utcnow().isoformat()

    counts = {
        'Signal': 0,
        'Scalar': 0,
        'Condition': 0,
        'Asset': 0,
        'Relationship': 0,
        'Overall': 0
    }

    total = len(metadata_df)

    def _print_push_progress():
        print('(%d/%d) %d signals, %d scalars, %d conditions, %d assets, %d relationships' %
              (counts['Overall'],
               total,
               counts['Signal'],
               counts['Scalar'],
               counts['Condition'],
               counts['Asset'],
               counts['Relationship']))

    flush_now = False
    cache = dict()
    roots = dict()
    batch_size = 1000
    put_signals_input = PutSignalsInputV1()
    put_signals_input.signals = list()
    put_scalars_input = PutScalarsInputV1()
    put_scalars_input.scalars = list()
    condition_batch_input = ConditionBatchInputV1()
    condition_batch_input.conditions = list()
    asset_batch_input = AssetBatchInputV1()
    asset_batch_input.assets = list()
    tree_batch_input = AssetTreeBatchInputV1()
    tree_batch_input.relationships = list()
    tree_batch_input.parent_host_id = datasource_output.id
    tree_batch_input.child_host_id = datasource_output.id
    last_scalar_datasource = None

    push_results_df = metadata_df.copy()
    for index, row in metadata_df.iterrows():
        counts['Overall'] += 1

        try:
            d = row.to_dict()

            if 'Name' not in d:
                raise Exception('Metadata must have a "Name" column.')

            if _common.get(d, 'Reference') is True:
                if not _common.present(d, 'ID'):
                    raise Exception('"ID" column required when "Reference" column is True')
                _build_reference(d)
                del d['ID']

            _type = None
            if not _common.present(d, 'Type'):
                raise Exception('"Type" column value is required')

            _type = d['Type']

            path = None
            if _common.present(d, 'Path'):
                path = d['Path']

            if _type != 'Asset':
                if _common.present(d, 'Path') != _common.present(d, 'Asset'):
                    raise Exception('"Asset" and "Path" columns must be paired for signals/conditions/scalars (can\'t '
                                    'include one without the other)')

                if _common.present(d, 'Asset'):
                    path += ' >> ' + d['Asset']

            if not _common.present(d, 'Data ID'):
                if path:
                    data_id = '%s >> %s' % (path, d['Name'])
                else:
                    data_id = d['Name']
            else:
                data_id = d['Data ID']

            if workbook_id:
                # Need to scope the Data ID it to the workbook so it doesn't collide with other workbooks
                d['Data ID'] = workbook_id + ' >> ' + six.text_type(data_id)

                d['Scoped To'] = workbook_id
            else:
                d['Data ID'] = data_id

            if not _common.present(d, 'Datasource Class'):
                d['Datasource Class'] = _common.DEFAULT_DATASOURCE_CLASS

            if not _common.present(d, 'Datasource ID'):
                d['Datasource ID'] = _common.DEFAULT_DATASOURCE_ID

            if 'Signal' in _type:
                signal_input = SignalInputV1() if _common.present(d, 'ID') else SignalWithIdInputV1()

                _dict_to_signal_input(d, signal_input)

                signal_input.formula_parameters = _process_formula_parameters(signal_input.formula_parameters)
                if len(signal_input.formula_parameters) > 0:
                    push_results_df.at[index, 'Formula Parameters'] = signal_input.formula_parameters

                signal_input.sync_token = sync_token

                if _common.present(d, 'ID'):
                    counts['Signal'] += 1
                    try:
                        signal_output = signals_api.put_signal(id=d['ID'], body=signal_input)  # type: SignalOutputV1
                        push_results_df.at[index, 'Push Result'] = 'Success'
                        push_results_df.at[index, 'ID'] = signal_output.id
                        push_results_df.at[index, 'Type'] = signal_output.type
                    except ApiException as e:
                        push_results_df.at[index, 'Push Result'] = e
                else:
                    signal_input.datasource_class = d['Datasource Class']
                    signal_input.datasource_id = d['Datasource ID']
                    signal_input.data_id = d['Data ID']
                    setattr(signal_input, 'dataframe_index', index)
                    counts['Signal'] += _add_no_dupe(put_signals_input.signals, signal_input)

            elif 'Scalar' in _type:
                scalar_input = ScalarInputV1()

                _dict_to_scalar_input(d, scalar_input)

                scalar_input.parameters = _process_formula_parameters(scalar_input.parameters)
                if len(scalar_input.parameters) > 0:
                    push_results_df.at[index, 'Formula Parameters'] = scalar_input.parameters

                put_scalars_input.datasource_class = d['Datasource Class']
                put_scalars_input.datasource_id = d['Datasource ID']
                scalar_input.data_id = d['Data ID']
                scalar_input.sync_token = sync_token
                setattr(scalar_input, 'dataframe_index', index)
                counts['Scalar'] += _add_no_dupe(put_scalars_input.scalars, scalar_input)

                # Since with scalars we have to put the Datasource Class and Datasource ID on the batch, we have to
                # recognize if it changed and, if so, flush the current batch.
                if last_scalar_datasource is not None and \
                        last_scalar_datasource != (d['Datasource Class'], d['Datasource ID']):
                    flush_now = True

                last_scalar_datasource = (d['Datasource Class'], d['Datasource ID'])

            elif 'Condition' in _type:
                condition_input = ConditionInputV1()
                _dict_to_condition_input(d, condition_input)

                condition_input.parameters = _process_formula_parameters(condition_input.parameters)
                if len(condition_input.parameters) > 0:
                    push_results_df.at[index, 'Formula Parameters'] = condition_input.parameters

                condition_input.datasource_class = d['Datasource Class']
                condition_input.datasource_id = d['Datasource ID']
                condition_input.data_id = d['Data ID']
                condition_input.sync_token = sync_token
                setattr(condition_input, 'dataframe_index', index)
                counts['Condition'] += _add_no_dupe(condition_batch_input.conditions, condition_input)

            elif _type == 'Asset':
                asset_input = AssetInputV1()
                _dict_to_asset_input(d, asset_input)

                asset_input.sync_token = sync_token
                setattr(asset_input, 'dataframe_index', index)
                counts['Asset'] += _add_no_dupe(asset_batch_input.assets, asset_input, overwrite=True)
                asset_batch_input.host_id = datasource_output.id

            if path:
                _reify_path(path, workbook_id, datasource_output, d['Data ID'], cache, roots,
                            asset_batch_input, tree_batch_input, sync_token, counts)

        except Exception as e:
            if errors == 'raise':
                raise

            total -= 1
            push_results_df.at[index, 'Push Result'] = e
            continue

        if counts['Overall'] % batch_size == 0 or flush_now:
            # clear_output(wait=True)
            _print_push_progress()

            _flush(put_signals_input, put_scalars_input, condition_batch_input, asset_batch_input, tree_batch_input,
                   push_results_df)

            flush_now = False

    _print_push_progress()

    _flush(put_signals_input, put_scalars_input, condition_batch_input, asset_batch_input, tree_batch_input,
           push_results_df)

    for asset_input in roots.values():
        results = items_api.search_items(filters=['Datasource Class==%s && Datasource ID==%s && Data ID==%s' % (
            _common.DEFAULT_DATASOURCE_CLASS, _common.DEFAULT_DATASOURCE_CLASS,
            asset_input.data_id)])  # type: ItemSearchPreviewPaginatedListV1
        if len(results.items) == 0:
            raise Exception('Root item "%s" not found' % asset_input.name)
        item_id_list = ItemIdListInputV1()
        item_id_list.items = [results.items[0].id]
        trees_api.move_nodes_to_root_of_tree(body=item_id_list)

    # clear_output(wait=True)

    if archive:
        print('Archiving outdated items...')
        datasource_clean_up_input = DatasourceCleanUpInputV1()
        datasource_clean_up_input.sync_token = sync_token
        datasources_api.clean_up(id=datasource_output.id, body=datasource_clean_up_input)

    # clear_output()

    return push_results_df


def _dict_to_input(d, _input, properties_attr, attr_map):
    for k, v in d.items():
        if k in attr_map:
            if attr_map[k] is not None:
                v = _common.get(d, k)
                if v is not None:
                    setattr(_input, attr_map[k], v)
        elif properties_attr is not None:
            p = ScalarPropertyV1()
            p.name = _common.ensure_unicode(k)
            uom = None
            if isinstance(v, dict):
                uom = _common.get(v, 'Unit Of Measure')
                v = _common.get(v, 'Value')
            else:
                v = _common.get(d, k)

            if v is not None:
                p.value = _common.ensure_unicode(v)
                if uom is not None:
                    p.unit_of_measure = _common.ensure_unicode(uom)
                _properties = getattr(_input, properties_attr)
                if _properties is None:
                    _properties = []
                _properties.append(p)
                setattr(_input, properties_attr, _properties)


def _dict_to_datasource_input(d, datasource_input):
    _dict_to_input(d, datasource_input, None, {
        'Name': 'name',
        'Description': 'description',
        'Datasource Name': 'name',
        'Datasource Class': 'datasource_class',
        'Datasource ID': 'datasource_id'
    })


def _dict_to_asset_input(d, asset_input):
    _dict_to_input(d, asset_input, 'properties', {
        'Type': None,
        'Name': 'name',
        'Description': 'description',
        'Datasource Class': 'datasource_class',
        'Datasource ID': 'datasource_id',
        'Data ID': 'data_id',
        'Scoped To': 'scoped_to'
    })


def _dict_to_signal_input(d, signal_input):
    _dict_to_input(d, signal_input, 'additional_properties', {
        'Type': None,
        'Name': 'name',
        'Description': 'description',
        'Datasource Class': 'datasource_class',
        'Datasource ID': 'datasource_id',
        'Data ID': 'data_id',
        'Data Version Check': 'data_version_check',
        'Formula': 'formula',
        'Formula Parameters': 'formula_parameters',
        'Interpolation Method': 'interpolation_method',
        'Maximum Interpolation': 'maximum_interpolation',
        'Scoped To': 'scoped_to',
        'Key Unit Of Measure': 'key_unit_of_measure',
        'Value Unit Of Measure': 'value_unit_of_measure',
        'Number Format': 'number_format'
    })


def _dict_to_scalar_input(d, scalar_input):
    _dict_to_input(d, scalar_input, 'additional_properties', {
        'Type': None,
        'Name': 'name',
        'Description': 'description',
        'Datasource Class': 'datasource_class',
        'Datasource ID': 'datasource_id',
        'Data ID': 'data_id',
        'Data Version Check': 'data_version_check',
        'Formula': 'formula',
        'Formula Parameters': 'parameters',
        'Scoped To': 'scoped_to',
        'Number Format': 'number_format'
    })


def _dict_to_condition_input(d, signal_input):
    _dict_to_input(d, signal_input, 'properties', {
        'Type': None,
        'Name': 'name',
        'Description': 'description',
        'Datasource Class': 'datasource_class',
        'Datasource ID': 'datasource_id',
        'Data ID': 'data_id',
        'Data Version Check': 'data_version_check',
        'Formula': 'formula',
        'Formula Parameters': 'parameters',
        'Maximum Duration': 'maximum_duration',
        'Scoped To': 'scoped_to'
    })


def _dict_to_capsule(d, capsule):
    _dict_to_input(d, capsule, 'properties', {
        'Capsule Start': None,
        'Capsule End': None
    })


def reify_workbook(workbook_path, create=True):
    workbooks_api = WorkbooksApi(_login.client)
    folders_api = FoldersApi(_login.client)

    workbook_path = re.split(r'\s*>>\s*', workbook_path)

    parent_id = None
    workbook_id = None
    for i in range(0, len(workbook_path)):
        existing_content_id = None
        content_name = workbook_path[i]
        content_type = 'Workbook' if i == len(workbook_path) - 1 else 'Folder'
        if parent_id:
            folders = folders_api.get_folders(filter='owner',
                                              folder_id=parent_id,
                                              limit=10000)  # type: FolderOutputListV1
        else:
            folders = folders_api.get_folders(filter='owner',
                                              limit=10000)  # type: FolderOutputListV1

        for content in folders.content:  # type: BaseOutput
            if content_type == content.type and content_name == content.name:
                existing_content_id = content.id
                break

        if not existing_content_id:
            if not create:
                return None

            if content_type == 'Folder':
                folder_input = FolderInputV1()
                folder_input.name = content_name
                folder_input.description = 'Created by Seeq Data Lab'
                folder_input.owner_id = _login.user.id
                folder_input.parent_folder_id = parent_id
                folder_output = folders_api.create_folder(body=folder_input)  # type: FolderOutputV1
                existing_content_id = folder_output.id
            else:
                workbook_input = WorkbookInputV1()
                workbook_input.name = content_name
                workbook_input.description = 'Created by Seeq Data Lab'
                workbook_input.owner_id = _login.user.id
                workbook_input.folder_id = parent_id
                workbook_output = workbooks_api.create_workbook(body=workbook_input)  # type: WorkbookOutputV1
                existing_content_id = workbook_output.id

        parent_id = existing_content_id
        workbook_id = existing_content_id

    return workbook_id


def _push_condition(condition_metadata, conditions_api, data, earliest_sample, latest_sample):
    condition_batch_input = ConditionBatchInputV1()
    condition_input = ConditionInputV1()
    _dict_to_condition_input(condition_metadata, condition_input)
    condition_batch_input.conditions = [condition_input]
    condition_input.datasource_class = condition_metadata['Datasource Class']
    condition_input.datasource_id = condition_metadata['Datasource ID']
    items_batch_output = conditions_api.put_conditions(body=condition_batch_input)  # type: ItemBatchOutputV1
    item_update_output = items_batch_output.item_updates[0]  # type: ItemUpdateOutputV1
    capsules_input = CapsulesInputV1()
    capsules_input.capsules = list()
    capsules_input.key_unit_of_measure = 'ns'
    count = 0
    for index, row in data.iterrows():
        capsule = CapsuleV1()
        _dict_to_capsule(row.to_dict(), capsule)
        capsule.start = row['Capsule Start'].value
        capsule.end = row['Capsule End'].value
        capsules_input.capsules.append(capsule)
        key_in_ms = capsule.start / 1000000
        earliest_sample = min(key_in_ms, earliest_sample) if earliest_sample is not None else key_in_ms
        key_in_ms = capsule.end / 1000000
        latest_sample = max(key_in_ms, latest_sample) if latest_sample is not None else key_in_ms

        if len(capsules_input.capsules) > _common.DEFAULT_PUT_SAMPLES_AND_CAPSULES_BATCH_SIZE:
            conditions_api.add_capsules(id=item_update_output.item.id, body=capsules_input)
            count += len(capsules_input.capsules)
            print('%s: Pushed %d capsules' % (condition_metadata['Name'], count))
            capsules_input.capsules = list()
    if len(capsules_input.capsules) > 0:
        conditions_api.add_capsules(id=item_update_output.item.id, body=capsules_input)
        count += len(capsules_input.capsules)
        print('%s: Pushed %d capsules' % (condition_metadata['Name'], count))
    return earliest_sample, latest_sample, item_update_output.item.id


def axis_number_from_string(axis):
    axis_number = 0
    exponent = 0
    while len(axis) > 0:
        alpha = axis[0]
        value = ord(alpha) - 65
        axis_number += value * 26 ** exponent
        exponent += 1
        axis = axis[0:-1]

    return axis_number


def string_from_axis_number(axis_number):
    axis = ''
    exponent = 0
    while axis_number > 0:
        axis = chr(int(axis_number % 26) + 65) + axis
        exponent += 1
        axis_number = axis_number / 26 ** exponent

    return axis


def _push_signal(column, signal_metadata, data, earliest_sample, latest_sample, signals_api, workstep_json,
                 type_mismatches):
    signal_input = SignalInputV1()
    _dict_to_signal_input(signal_metadata, signal_input)
    put_samples_input = PutSamplesInputV1()
    put_samples_input.samples = list()
    count = 0
    is_string = None
    signal_output = None
    for index, row in data.iterrows():
        if pd.isna(row[column]):
            continue

        sample_value = row[column]

        if is_string is None:
            if 'Value Unit Of Measure' in signal_metadata:
                is_string = (signal_metadata['Value Unit Of Measure'] == 'string')
            else:
                is_string = isinstance(sample_value, six.string_types)

        if is_string != isinstance(sample_value, six.string_types):
            try:
                if is_string:
                    sample_value = six.text_type(sample_value)
                else:
                    if data[column].dtype.name == 'int64':
                        sample_value = int(sample_value)
                    else:
                        sample_value = float(sample_value)
            except:
                # Couldn't convert it, fall through to the next conditional
                pass

        if is_string != isinstance(sample_value, six.string_types):
            if type_mismatches == 'drop':
                continue
            elif type_mismatches == 'raise':
                raise Exception('Column "%s" was detected as %s, but %s value at (%s, %s) found. Supply '
                                'type_mismatches parameter as "drop" to ignore the sample entirely or '
                                '"invalid" to insert an INVALID sample in its place.' %
                                (column, 'string-valued' if is_string else 'numeric-valued',
                                 'numeric' if is_string else 'string',
                                 index, sample_value))
            else:
                sample_value = None

        if isinstance(sample_value, np.number):
            sample_value = sample_value.item()

        if not signal_output:
            if is_string:
                signal_input.value_unit_of_measure = 'string'

            signal_output = signals_api.put_signal_by_data_id(datasource_class=signal_metadata['Datasource Class'],
                                                              datasource_id=signal_metadata['Datasource ID'],
                                                              data_id=signal_metadata['Data ID'],
                                                              body=signal_input)  # type: SignalOutputV1

        sample_input = SampleInputV1()
        key_in_ms = index.value / 1000000
        earliest_sample = min(key_in_ms, earliest_sample) if earliest_sample is not None else key_in_ms
        latest_sample = max(key_in_ms, latest_sample) if latest_sample is not None else key_in_ms

        sample_input.key = index.value
        sample_input.value = sample_value
        put_samples_input.samples.append(sample_input)

        if len(put_samples_input.samples) >= _common.DEFAULT_PUT_SAMPLES_AND_CAPSULES_BATCH_SIZE:
            signals_api.put_samples(id=signal_output.id,
                                    body=put_samples_input)
            count += len(put_samples_input.samples)
            print('%s: Pushed %d samples' % (signal_metadata['Name'], count))
            put_samples_input.samples = list()

        if workstep_json and len(workstep_json['state']['stores']['sqTrendSeriesStore']['items']) < 15:
            highest_lane = 1
            highest_axis = 0
            found = False
            for item in workstep_json['state']['stores']['sqTrendSeriesStore']['items']:
                if item['id'] == signal_output.id:
                    found = True

                if 'lane' in item:
                    highest_lane = max(item['lane'], highest_lane)

                if 'axisAlign' in item:
                    highest_axis = max(axis_number_from_string(item['axisAlign']), highest_axis)

            if not found:
                workstep_json['state']['stores']['sqTrendSeriesStore']['items'].append({
                    "axisAlign": string_from_axis_number(highest_axis + 1),
                    "axisAutoScale": True,
                    "id": signal_output.id,
                    "lane": highest_lane + 1
                })

    if len(put_samples_input.samples) > 0:
        signals_api.put_samples(id=signal_output.id,
                                body=put_samples_input)
        count += len(put_samples_input.samples)
        print('%s: Pushed %d samples' % (signal_metadata['Name'], count))

    return earliest_sample, latest_sample, signal_output.id


def _build_reference_signal(definition):
    definition['Type'] = 'CalculatedSignal'
    definition['Formula'] = '$signal'

    if _common.present(definition, 'Interpolation Method'):
        definition['Formula'] += ".to%s()" % definition['Interpolation Method']

    definition['Formula Parameters'] = 'signal=%s' % definition['ID']
    definition['Cache Enabled'] = False

    for key in ['ID', 'Datasource Class', 'Datasource ID', 'Data ID', 'Value Unit Of Measure',
                'Interpolation Method']:
        if _common.present(definition, key) and not _common.present(definition, 'Referenced ' + key):
            definition['Referenced ' + key] = definition[key]
            del definition[key]


def _build_reference_condition(definition):
    definition['Type'] = 'CalculatedCondition'
    definition['Formula'] = '$condition'

    definition['Formula Parameters'] = 'condition=%s' % definition['ID']
    definition['Cache Enabled'] = False

    for key in ['ID', 'Datasource Class', 'Datasource ID', 'Data ID', 'Unit Of Measure', 'Maximum Duration']:
        if _common.present(definition, key) and not _common.present(definition, 'Referenced ' + key):
            definition['Referenced ' + key] = definition[key]
            del definition[key]


def _build_reference(definition):
    {
        'StoredSignal': _build_reference_signal,
        'StoredCondition': _build_reference_condition
    }[definition['Type']](definition)


def _process_formula_parameters(parameters):
    if parameters is None:
        return list()

    if isinstance(parameters, dict):
        parameters_dict = parameters  # type: dict
        return _parameters_dict_to_list(parameters_dict)

    if not isinstance(parameters, list):
        return [parameters]


def _parameters_dict_to_list(parameters_dict):
    parameters_list = list()
    for k, v in parameters_dict.items():
        # Strip off leading dollar-sign if it's there
        parameter_name = re.sub(r'^\$', '', k)
        if isinstance(v, pd.DataFrame):
            parameter_id = v.iloc[0]['ID']
        else:
            parameter_id = v
        parameters_list.append('%s=%s' % (parameter_name, parameter_id))

    return parameters_list


def _flush(put_signals_input, put_scalars_input, condition_batch_input, asset_batch_input, tree_batch_input,
           push_results_df):
    signals_api = SignalsApi(_login.client)
    scalars_api = ScalarsApi(_login.client)
    conditions_api = ConditionsApi(_login.client)
    assets_api = AssetsApi(_login.client)
    trees_api = TreesApi(_login.client)

    def _set_push_result_string(dfi, iuo):
        s = 'Success' if iuo.error_message is None else iuo.error_message
        push_results_df.at[dfi, 'Push Result'] = s
        if iuo.item is not None:
            push_results_df.at[dfi, 'ID'] = iuo.item.id
            push_results_df.at[dfi, 'Type'] = iuo.item.type

    if len(put_signals_input.signals) > 0:
        item_batch_output = signals_api.put_signals(body=put_signals_input)  # type: ItemBatchOutputV1
        for i in range(0, len(put_signals_input.signals)):
            signal_input = put_signals_input.signals[i]
            item_update_output = item_batch_output.item_updates[i]  # type: ItemUpdateOutputV1
            _set_push_result_string(signal_input.dataframe_index, item_update_output)

        put_signals_input.signals = list()

    if len(put_scalars_input.scalars) > 0:
        item_batch_output = scalars_api.put_scalars(body=put_scalars_input)  # type: ItemBatchOutputV1
        for i in range(0, len(put_scalars_input.scalars)):
            scalar_input = put_scalars_input.scalars[i]
            item_update_output = item_batch_output.item_updates[i]  # type: ItemUpdateOutputV1
            _set_push_result_string(scalar_input.dataframe_index, item_update_output)

        put_scalars_input.scalars = list()

    if len(condition_batch_input.conditions) > 0:
        item_batch_output = conditions_api.put_conditions(body=condition_batch_input)  # type: ItemBatchOutputV1
        for i in range(0, len(condition_batch_input.conditions)):
            condition_input = condition_batch_input.conditions[i]
            item_update_output = item_batch_output.item_updates[i]  # type: ItemUpdateOutputV1
            _set_push_result_string(condition_input.dataframe_index, item_update_output)

        condition_batch_input.conditions = list()

    if len(asset_batch_input.assets) > 0:
        item_batch_output = assets_api.batch_create_assets(body=asset_batch_input)  # type: ItemBatchOutputV1
        for i in range(0, len(asset_batch_input.assets)):
            asset_input = asset_batch_input.assets[i]
            if not hasattr(asset_input, 'dataframe_index'):
                continue
            item_update_output = item_batch_output.item_updates[i]  # type: ItemUpdateOutputV1
            _set_push_result_string(asset_input.dataframe_index, item_update_output)

        asset_batch_input.assets = list()

    if len(tree_batch_input.relationships) > 0:
        trees_api.batch_move_nodes_to_parents(body=tree_batch_input)  # type: ItemBatchOutputV1
        tree_batch_input.relationships = list()


def _add_no_dupe(lst, obj, attr='data_id', overwrite=False):
    for i in range(0, len(lst)):
        o = lst[i]
        if hasattr(o, attr):
            if getattr(o, attr) == getattr(obj, attr):
                if overwrite:
                    lst[i] = obj
                return 0

    lst.append(obj)
    return 1


def _reify_path(path, workbook_id, datasource_output, scoped_data_id, cache, roots, asset_batch_input,
                tree_batch_input, sync_token, counts):
    path_items = re.split(r'\s*>>\s*', path)

    path_so_far = workbook_id
    for path_item in path_items:
        asset_input = AssetInputV1()
        asset_input.name = path_item
        asset_input.scoped_to = workbook_id
        asset_input.host_id = datasource_output.id
        asset_input.sync_token = sync_token

        tree_input = AssetTreeSingleInputV1()
        tree_input.parent_data_id = path_so_far

        path_so_far += ' >> ' + path_item
        asset_input.data_id = path_so_far
        tree_input.child_data_id = path_so_far

        if asset_input.data_id not in cache:
            if tree_input.parent_data_id != workbook_id:
                counts['Relationship'] += 1
                tree_batch_input.relationships.append(tree_input)
            else:
                roots[asset_input.data_id] = asset_input

            counts['Asset'] += _add_no_dupe(asset_batch_input.assets, asset_input)

            cache[asset_input.data_id] = True

    tree_input = AssetTreeSingleInputV1()
    tree_input.parent_data_id = path_so_far
    tree_input.child_data_id = scoped_data_id
    counts['Relationship'] += _add_no_dupe(tree_batch_input.relationships, tree_input, 'child_data_id')
