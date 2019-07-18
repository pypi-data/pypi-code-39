import queue
import threading

import pandas as pd
import numpy as np

from seeq.sdk import *

from . import _common
from . import _login


def pull(items, start=None, end=None, grid='15min', header='__auto__', capsules_as='auto', tz_convert=None):
    if not isinstance(items, pd.DataFrame):
        print('"items" must be a pandas.DataFrame')
        return

    if end is None:
        end = pd.datetime.now()
        if start is not None and start > end:
            end = start + pd.Timedelta(hours=1)

    if start is None:
        start = pd.datetime.now() if end is None else end
        start = start - pd.Timedelta(hours=1)

    pd_start = pd.to_datetime(start)  # type: pd.Timestamp
    pd_end = pd.to_datetime(end)  # type: pd.Timestamp

    items_api = ItemsApi(_login.client)
    formulas_api = FormulasApi(_login.client)

    query_df = items  # type: pd.DataFrame
    output_df = pd.DataFrame()
    at_least_one_signal = False
    column_names = list()
    for phase in ['signals', 'conditions', 'scalars']:
        threads = list()
        pulled_series = queue.Queue()
        total_capsules = 0
        for index, row in query_df.iterrows():
            if phase == 'signals' and not _common.present(row, 'ID'):
                print('Row "%s" does not contain a value for "ID", skipping' % index)
                continue

            item_id, item_name, item_type = _get_item_details(header, items_api, query_df, row)

            if phase == 'signals' and \
                    'Signal' not in item_type and 'Condition' not in item_type and 'Scalar' not in item_type:
                print('Item with ID "%s" is not a Signal, Condition or Scalar, skipping' % row['ID'])
                continue

            if 'Signal' in item_type:
                at_least_one_signal = True

            if phase == 'signals' and 'Signal' in item_type:

                parameters = ['signal=%s' % item_id]
                if 'Calculate' in row and not pd.isna(row['Calculate']):
                    formula = row['Calculate']
                else:
                    formula = '$signal'

                if grid:
                    formula = 'resample(%s, %s)' % (formula, grid)

                thread = threading.Thread(target=_pull_signal, args=(formulas_api, formula, parameters,
                                                                     item_name, pulled_series, pd_start, pd_end,
                                                                     tz_convert))

                thread.start()

                threads.append(thread)

            elif phase == 'conditions' and 'Condition' in item_type:
                if capsules_as == 'capsules' and at_least_one_signal:
                    raise Exception('Pull cannot include signals when conditions present and "capsules_as" '
                                    'parameter is "capsules"')

                if capsules_as == 'auto':
                    capsules_as = 'signals' if at_least_one_signal else 'capsules'

                if capsules_as == 'signals' and not at_least_one_signal:
                    if grid is None:
                        raise Exception('Pull cannot include conditions when no signals present with capsules_as='
                                        'capsules and grid=None')

                    placeholder_item_name = '__placeholder__'
                    _pull_signal(formulas_api, '0.toSignal(%s)' % grid, list(), placeholder_item_name,
                                 pulled_series, pd_start, pd_end, tz_convert)

                    _, series = pulled_series.get()
                    output_df[placeholder_item_name] = series

                parameters = ['condition=%s' % item_id]
                if 'Calculate' in row and not pd.isna(row['Calculate']):
                    formula = row['Calculate']
                else:
                    formula = '$condition'

                _pull_condition(capsules_as, formulas_api, formula, parameters, item_name, output_df,
                                pd_start, pd_end, total_capsules, tz_convert)

            elif phase == 'scalars' and 'Scalar' in item_type:
                parameters = ['scalar=%s' % item_id]
                if 'Calculate' in row and not pd.isna(row['Calculate']):
                    formula = row['Calculate']
                else:
                    formula = '$scalar'

                _pull_scalar(formulas_api, formula, parameters, item_name, output_df, pd_end)

            if phase == 'scalars':
                if 'Condition' in item_type and capsules_as == 'capsules':
                    if 'Condition' not in column_names:
                        column_names.append('Condition')
                    if 'Capsule Start' not in column_names:
                        column_names.append('Capsule Start')
                    if 'Capsule End' not in column_names:
                        column_names.append('Capsule End')
                else:
                    column_names.append(item_name)

        for thread in threads:
            thread.join()

        for item_name, series in list(pulled_series.queue):
            output_df[item_name] = series

    # Ensures that the order of the columns matches the order in the metadata
    return output_df[column_names]


def _convert_timestamp_timezone(timestamp, tz):
    if pd.isna(timestamp):
        return timestamp

    timestamp = timestamp.tz_localize('UTC')
    return timestamp.tz_convert(tz) if tz else timestamp


def _convert_column_timezone(ts_column, tz):
    ts_column = ts_column.tz_localize('UTC')
    return ts_column.tz_convert(tz) if tz else ts_column


def _pull_condition(capsules_as, formulas_api, formula, parameters, item_name, output_df, pd_start, pd_end,
                    total_capsules, tz):
    offset = 0
    while True:
        formula_run_output, _, http_headers = formulas_api.run_formula_with_http_info(
            formula=formula,
            parameters=parameters,
            start='%d ns' % pd_start.value,
            end='%d ns' % pd_end.value,
            offset=offset,
            limit=_common.DEFAULT_PULL_PAGE_SIZE)  # type: FormulaRunOutputV1

        capsules_output = formula_run_output.capsules  # type: CapsulesOutputV1

        def _c(dt):
            return _convert_timestamp_timezone(_common.none_to_nan(pd.to_datetime(dt)), tz)

        columns = dict()
        if capsules_as == 'signals':
            columns[item_name] = pd.Series()
            starting_capsule_index = 0
            for _index, _ in output_df.iterrows():
                for i in range(starting_capsule_index, len(capsules_output.capsules)):
                    capsule = capsules_output.capsules[i]  # type: CapsuleV1
                    capsule_start = _index if pd.isna(capsule.start) else _c(capsule.start)
                    capsule_end = _index if pd.isna(capsule.end) else _c(capsule.end)
                    present = capsule_start <= _index <= capsule_end
                    if capsule_end < _index:
                        starting_capsule_index = i
                    columns[item_name].at[_index] = 1 if present else 0
                    for prop in capsule.properties:  # type: ScalarPropertyV1
                        colname = '%s - %s' % (item_name, prop.name)
                        if colname not in columns:
                            columns[colname] = pd.Series()
                        columns[colname].at[_index] = prop.value if present else np.nan

            for col, series in columns.items():
                output_df[col] = series
        else:
            for capsule in capsules_output.capsules:
                output_df.at[total_capsules, 'Condition'] = item_name
                output_df.at[total_capsules, 'Capsule Start'] = _c(capsule.start)
                output_df.at[total_capsules, 'Capsule End'] = _c(capsule.end)
                for prop in capsule.properties:  # type: ScalarPropertyV1
                    output_df.at[total_capsules, prop.name] = prop.value

                total_capsules += 1

        if len(capsules_output.capsules) < _common.DEFAULT_PULL_PAGE_SIZE:
            break

        offset += len(capsules_output.capsules)


def _pull_signal(formulas_api, formula, parameters, item_name, pulled_series, pd_start, pd_end, tz):
    series = pd.Series()
    offset = 0
    while True:
        formula_run_output, _, http_headers = formulas_api.run_formula_with_http_info(
            formula=formula,
            parameters=parameters,
            start='%d ns' % pd_start.value,
            end='%d ns' % pd_end.value,
            offset=offset,
            limit=_common.DEFAULT_PULL_PAGE_SIZE)  # type: FormulaRunOutputV1

        timings = _common.get_timings(http_headers)

        series_samples_output = formula_run_output.samples  # type: SeriesSamplesOutputV1

        time_index = _convert_column_timezone(pd.DatetimeIndex([sample_output.key for sample_output in
                                                                series_samples_output.samples]), tz)
        series = series.append(pd.Series([_common.none_to_nan(sample_output.value) for sample_output in
                                          series_samples_output.samples], index=time_index))

        if len(series_samples_output.samples) < _common.DEFAULT_PULL_PAGE_SIZE:
            break

        offset += len(series_samples_output.samples)

    pulled_series.put((item_name, series))


def _pull_scalar(formulas_api, formula, parameters, item_name, output_df, pd_end):
    formula_run_output, _, http_headers = formulas_api.run_formula_with_http_info(
        formula=formula,
        parameters=parameters)  # type: FormulaRunOutputV1

    if len(output_df.index) == 0:
        output_df.at[0, item_name] = formula_run_output.scalar.value
    else:
        output_df[item_name] = formula_run_output.scalar.value


def _get_item_details(header, items_api, query_df, row):
    item_id = _common.get(row, 'ID')
    item = None
    if 'Type' in query_df.columns:
        item_type = row['Type']
    else:
        item = items_api.get_item_and_all_properties(id=item_id)  # type: ItemOutputV1
        item_type = item.type
    if header.upper() == 'ID':
        item_name = item_id
    elif header in query_df.columns:
        item_name = row[header]
    else:
        if not item:
            item = items_api.get_item_and_all_properties(id=item_id)  # type: ItemOutputV1

        item_name = ''
        if header == '__auto__' and _common.present(row, 'Path'):
            item_name = row['Path'] + ' >> '
            if _common.present(row, 'Asset'):
                item_name += row['Asset'] + ' >> '

        if header in ['__auto__', 'Name']:
            item_name += item.name
        elif header == 'Description':
            item_name += item.description
        else:
            prop = [p.value for p in item.properties if p.name == header]
            if len(prop) == 0:
                item_name += item_id
            else:
                item_name += prop[0]

    return item_id, item_name, item_type
