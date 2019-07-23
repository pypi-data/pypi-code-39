import re
import json
import copy
import sys
import datetime
from decimal import Decimal
import numpy as np
import pandas as pd
import gzip


def null_test(var):
    ret_val = None
    if var is None:
        ret_val = None  # redundant but explicit
    elif isinstance(var, list) and len(var) == 0:
        ret_val = None  # redundant but explicit
    elif isinstance(var, dict) and len(var.keys()) == 0:
        ret_val = None  # redundant but explicit
    elif isinstance(var, (np.ndarray, list)) and pd.isnull(var).all():
        ret_val = None  # redundant but explicit
    elif not isinstance(var, (np.ndarray, list)) and pd.isnull(var):
        ret_val = None  # redundant but explicit
    else:
        ret_val = var

    return ret_val


def list_to_quoted_delimited(input_list: list, delimiter: str = ',') -> str:
    """
    Returns a string which is quoted + delimited from a list
    :param input_list: eg: ['a', 'b', 'c']
    :param delimiter: '|'
    :return: eg: 'a'|'b'|'c'
    """
    return f'{delimiter} '.join("'{0}'".format(str_item) for str_item in input_list)


def flatten_json_to_table_fixed_keys(dictionary: dict, existence: bool = False) -> dict:
    """
    Wrapper to flatten nested JSON fields. Useful for noSQL to RDS conversions.
    Assumption: There is no column with pipeline character in the name.
    Handles Lists/Dicts while nested. Uses ~ to concat nested names as underscore is common in names
    :param dictionary: original nested JSON/Dict
    :param existence: flag to indicate if parent exists
    :return: flattened dictionary
    """

    def _flatten_json_to_table(structure, key="", path="", flattened=None):
        if flattened is None:
            flattened = {}
        if type(structure) not in (dict, list):
            if type(structure) is float:
                flattened[((path + "~") if path else "") + key] = round(structure, 9)
            else:
                flattened[((path + "~") if path else "") + key] = structure
        elif isinstance(structure, list):
            for i, item in enumerate(structure):
                _flatten_json_to_table(item, "|%d~" % i, path + "~" + key, flattened)
        else:
            for new_key, value in structure.items():
                _flatten_json_to_table(value, new_key, path + "~" + key, flattened)
        return flattened

    flat_dictionary = _flatten_json_to_table(dictionary)
    orig_keys = set(flat_dictionary.keys())
    fixed_keys = set([re.sub(' +', '~', key.strip('_')) for key in flat_dictionary.keys()])
    if len(orig_keys) == len(fixed_keys) and not existence:
        return {re.sub('~+', '~', key.strip('~')): value for key, value in sorted(flat_dictionary.items())}
    else:
        return flat_dictionary


def flatten_lists_all_level(list_of_lists: list) -> list:
    """
    Wrapper to unravel or flatten list of lists to max possible levels
    Can lead to RecursionError: maximum recursion depth exceeded
    Default = 1000, To increase (to say 1500): sys.setrecursionlimit(1500)
    """
    if not isinstance(list_of_lists, list):
        return list_of_lists
    elif len(list_of_lists) is 0:
        return []
    elif isinstance(list_of_lists[0], list):
        return flatten_lists_all_level(list_of_lists[0]) + flatten_lists_all_level(list_of_lists[1:])
    else:
        return [list_of_lists[0]] + flatten_lists_all_level(list_of_lists[1:])


def flatten_lists_one_level(potential_list_of_lists):
    """
    Wrapper to unravel or flatten list of lists only 1 level
    :param potential_list_of_lists: list containing lists
    :return: flattened list
    """
    flat_list = []
    for potential_list in potential_list_of_lists:
        if isinstance(potential_list, list):
            flat_list.extend(potential_list)
        else:
            flat_list.append(potential_list)
    return flat_list


def clean_dictionary(log, d, bq_fix: bool = True, bq_c_fix: dict = None, already_flat: bool = False):
    """
    Removes keys from dictionary recursively which are empty i.e. {}, [], None.
    Optionally fixes bq column names and custom fixes.
    :param log: logger obj
    :param d: dictionary to be cleaned
    :param bq_fix: Boolean flag to fix for bq or not
    :param bq_c_fix: None/Dict for custom bq datatype fix
    :param already_flat: Boolean if dict is already flattened
    :return: cleaned dictionary along with bq_fix/bq_c_fix as specified
    """
    rep_char = '_bi_'

    def _bq_num_start_fix(colval):
        prefixed = colval
        if colval[0].isdigit():
            prefixed = f'bi_{colval}'
        # return prefixed.replace('::', rep_char).replace('~', rep_char).replace('-', rep_char).lower()
        return re.sub('([^a-zA-Z0-9_]+)', rep_char, prefixed)

    def _bq_numeric_overflow_fix(colval):
        if isinstance(colval, float):
            return round(colval, 9)
        elif isinstance(colval, (datetime.datetime, datetime.date)):
            return str(colval)
        return colval

    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [v for v in (clean_dictionary(log, v, bq_fix=bq_fix) for v in d) if (v or isinstance(v, bool))]
    if bq_fix:
        ret_dict = {_bq_num_start_fix(k): _bq_numeric_overflow_fix(v)
                    for k, v in ((k, clean_dictionary(log, v, bq_fix=True)) for k, v in d.items())
                    if null_test(v) is not None and k != ''
                    }
    else:
        # ret_dict = {k: v for k, v in ((k, clean_dictionary(log, v, bq_fix=False))
        #                               for k, v in d.items()) if (v or isinstance(v, bool))}
        # log.info('bq_fix is set to False')
        # sys.exit(1)
        ret_dict = d

    if bq_c_fix and isinstance(bq_c_fix, dict):
        ret_dict = dict_bq_c_fix(ret_dict, bq_c_fix, already_flat=already_flat)

    return ret_dict


def json_serializer(o):
    """
    Func that gets called for objects that can't be JSON serialized
    :param o: obj to be serialized
    :return: JSON encodable version of o
    """
    if isinstance(o, datetime.datetime):
        try:
            return o.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return None
    elif isinstance(o, Decimal):
        return float(o)
    elif isinstance(o, np.int64):
        return int(o)


def dump_json_list_to_ndjson(log, json_, local_file_path: str, bq_fix: bool = True, bq_c_fix: dict = None,
                             already_flat: bool = False, **kwargs):
    """
    Dump List of  Dicts to NDJSON (Newline Delimited JSON)
    :param log: logger obj
    :param json_: List of Dicts
    :param local_file_path: local file path
    :param bq_fix: Boolean flag to fix for bq or not
    :param bq_c_fix: None/Dict for custom bq datatype fix
    :param already_flat: Bool if dict is already flat
    :param kwargs: dynamic capture of args
        :compression: gzip compression Boolean
    :return: None
    """
    log.info(f'Dumping json list as file to: {local_file_path}')
    if 'compression' in kwargs.keys():
        with gzip.open(local_file_path, 'wt', encoding='utf-8') as fp:
            for d in json_:
                json.dump(clean_dictionary(log, d, bq_fix=bq_fix, bq_c_fix=bq_c_fix, already_flat=already_flat), fp,
                          default=json_serializer)
                fp.write('\n')
    else:
        with open(local_file_path, 'w', encoding='utf-8') as fp:
            for d in json_:
                json.dump(clean_dictionary(log, d, bq_fix=bq_fix, bq_c_fix=bq_c_fix, already_flat=already_flat), fp,
                          default=json_serializer)
                fp.write('\n')


def dict_bq_c_fix(orig_dict, bq_c_fix, rep_char: str = '_bi_', already_flat: bool = False):
    if not already_flat:
        flat_d2 = flatten_json_to_table_fixed_keys(orig_dict)
        flat_d1 = copy.deepcopy(flat_d2)
        for k, v in flat_d1.items():
            kmatch = re.sub('(\.+)', '.', re.sub('\|[0-9]+', '.', k).replace('~', '.')).strip('.')
            # if kmatch in list(bq_c_fix.keys()) or kmatch in [_val.replace('.', '') for _val in list(bq_c_fix.keys())]:
            if kmatch in list(bq_c_fix.keys()):
                temp_flat_d1 = orig_dict
                ksplit = k.split('~')
                ksplit = ksplit[:-1] if ksplit[-1].replace('|', '').isdigit() else ksplit
                for kidx, parts in enumerate(ksplit):
                    use_parts = int(parts.replace('|', '')) if '|' in parts else parts
                    if kidx + 1 == len(ksplit):
                        temp_flat_d1[use_parts] = bq_c_fix[kmatch](temp_flat_d1[use_parts])
                    else:
                        temp_flat_d1 = temp_flat_d1[use_parts]
    else:
        flat_d1 = copy.deepcopy(orig_dict)
        for k, v in flat_d1.items():
            kmatch = re.sub('(\.+)', '.', re.sub('\|[0-9]+', '.', k).replace(rep_char, '.')).strip('.')
            if kmatch in list(bq_c_fix.keys()):
                orig_dict[k] = bq_c_fix[kmatch](orig_dict[k])
            else:
                pass

    return orig_dict


def dict_merge(_dct, merge_dct, add_keys=True, samples=-1):
    """
    Recursive dict merge. Instead of updating only top-level keys, dict_merge recurses down
    into dicts nested to an arbitrary depth, updating keys.
    The merge_dct is merged into _dct but returns a copy of the dictionary and leave the original arguments untouched.

    :param _dct: base dict onto which the merge is executed
    :param merge_dct: dict which is to be merged into the base dict
    :param add_keys: determines whether keys which are present in merge_dict but not _dct should be included in the
    :param samples: if -1 no sampling, else samples the volume of data specified
    :return: copy of the dictionary which merge operation completed
    """
    samples = -1 if samples <= 10 else samples
    dct = copy.deepcopy(_dct)
    if not add_keys:
        merge_dct = {k: merge_dct[k] for k in set(dct).intersection(set(merge_dct))}

    for k, v in merge_dct.items():
        if isinstance(dct.get(k), dict) and isinstance(v, dict):
            dct[k] = dict_merge(dct[k], v, add_keys=add_keys, samples=samples)
        elif isinstance(dct.get(k), list) and isinstance(v, list):
            if k in dct.keys():
                if samples == -1:
                    dct[k].append(v)
                elif len(dct[k]) <= samples:
                    dct[k].append(v)
                else:
                    pass
            else:
                dct[k] = [v]
        else:
            if k in dct.keys():
                if isinstance(dct[k], list):
                    if samples == -1:
                        dct[k].append(v)
                    elif len(dct[k]) <= samples:
                        dct[k].append(v)
                    else:
                        pass
                elif isinstance(dct[k], dict):
                    print('*** WARNING ****. Unexpected situation for dct[k] as type dict.')
                else:
                    print(f'*** WARNING ****. Unexpected situation. Non list/dict type for dct[k]: {type(dct[k])}')
            else:
                if isinstance(v, dict):
                    dct[k] = {_k: [_v] if not isinstance(_v, dict) else dict_merge({}, _v, add_keys, samples=samples)
                              for _k, _v in v.items()}
                else:
                    dct[k] = [v]

    return dct
