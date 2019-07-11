import queue
import threading

import pandas as pd
import numpy as np

from seeq.sdk import *

from . import _common
from . import _login


def pull(items, start, end, grid='15min', header='__auto__', capsules_as='auto'):
    if not isinstance(items, pd.DataFrame):
        print('"items" must be a pandas.DataFrame')
        return

    pd_start = pd.to_datetime(start)  # type: pd.Timestamp
    pd_end = pd.to_datetime(end)  # type: pd.Timestamp

    items_api = ItemsApi(_login.client)
    formulas_api = FormulasApi(_login.client)

    query_df = items  # type: pd.DataFrame
    output_df = pd.DataFrame()
    at_least_one_signal = False
    for phase in ['signals', 'conditions']:
        threads = list()
        fetched_series = queue.Queue()
        total_capsules = 0
        for index, row in query_df.iterrows():
            if not _common.present(row, 'ID'):
                print('Row "%s" does not contain a value for "ID", skipping' % index)
                continue

            item_id, item_name, item_type = _get_item_details(header, items_api, query_df, row)

            if 'Signal' in item_type:
                at_least_one_signal = True

            if phase == 'signals' and 'Signal' in item_type:

                thread = threading.Thread(target=_fetch_signal, args=(formulas_api, grid, item_id, item_name,
                                                                      fetched_series, pd_start, pd_end, row))

                thread.start()

                threads.append(thread)

            elif phase == 'conditions' and 'Condition' in item_type:
                _fetch_condition(at_least_one_signal, capsules_as, formulas_api, item_id, item_name, output_df, pd_end,
                                 pd_start, row, total_capsules)

        for thread in threads:
            thread.join()

        for item_name, series in list(fetched_series.queue):
            output_df[item_name] = series

    return output_df


def _fetch_condition(at_least_one_signal, capsules_as, formulas_api, item_id, item_name, output_df, pd_end, pd_start,
                     row, total_capsules):
    if capsules_as == 'capsules' and at_least_one_signal:
        raise Exception('Fetch cannot include signals when conditions present and "capsules_as" '
                        'parameter is "capsules"')
    elif capsules_as == 'signals' and not at_least_one_signal:
        raise Exception('Fetch must include at least one signal when conditions present and "capsules_as" '
                        'parameter is "signals" or "auto')
    if capsules_as == 'auto':
        capsules_as = 'signals' if at_least_one_signal else 'capsules'
    parameter = 'condition=%s' % item_id
    if 'Calculate' in row and not pd.isna(row['Calculate']):
        formula = row['Calculate']
    else:
        formula = '$condition'
    offset = 0
    while True:
        formula_run_output, _, http_headers = formulas_api.run_formula_with_http_info(
            formula=formula,
            parameters=[parameter],
            start='%d ns' % pd_start.value,
            end='%d ns' % pd_end.value,
            offset=offset,
            limit=_common.DEFAULT_FETCH_PAGE_SIZE)  # type: FormulaRunOutputV1

        capsules_output = formula_run_output.capsules  # type: CapsulesOutputV1

        columns = dict()
        if capsules_as == 'signals':
            columns[item_name] = pd.Series()
            starting_capsule_index = 0
            for _index, _ in output_df.iterrows():
                for i in range(starting_capsule_index, len(capsules_output.capsules)):
                    capsule = capsules_output.capsules[i]  # type: CapsuleV1
                    capsule_start = pd.to_datetime(capsule.start)
                    capsule_end = pd.to_datetime(capsule.end)
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
                output_df.at[total_capsules, 'Capsule Start'] = pd.to_datetime(capsule.start)
                output_df.at[total_capsules, 'Capsule End'] = pd.to_datetime(capsule.end)
                for prop in capsule.properties:  # type: ScalarPropertyV1
                    output_df.at[total_capsules, prop.name] = prop.value

                total_capsules += 1

        if len(capsules_output.capsules) < _common.DEFAULT_FETCH_PAGE_SIZE:
            break

        offset += len(capsules_output.capsules)


def _fetch_signal(formulas_api, grid, item_id, item_name, fetched_series, pd_start, pd_end, row):
    parameter = 'signal=%s' % item_id
    if 'Calculate' in row and not pd.isna(row['Calculate']):
        formula = row['Calculate']
    else:
        formula = '$signal'
    if grid:
        formula = 'resample(%s, %s)' % (formula, grid)

    series = pd.Series()
    offset = 0
    while True:
        formula_run_output, _, http_headers = formulas_api.run_formula_with_http_info(
            formula=formula,
            parameters=[parameter],
            start='%d ns' % pd_start.value,
            end='%d ns' % pd_end.value,
            offset=offset,
            limit=_common.DEFAULT_FETCH_PAGE_SIZE)  # type: FormulaRunOutputV1

        timings = _common.get_timings(http_headers)

        series_samples_output = formula_run_output.samples  # type: SeriesSamplesOutputV1

        def none_to_nan(v):
            return np.nan if v is None else v

        series = series.append(pd.Series([none_to_nan(sample_output.value) for sample_output in
                                          series_samples_output.samples],
                                         index=pd.DatetimeIndex([sample_output.key for sample_output
                                                                 in series_samples_output.samples])))

        if len(series_samples_output.samples) < _common.DEFAULT_FETCH_PAGE_SIZE:
            break

        offset += len(series_samples_output.samples)

    fetched_series.put((item_name, series))


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
