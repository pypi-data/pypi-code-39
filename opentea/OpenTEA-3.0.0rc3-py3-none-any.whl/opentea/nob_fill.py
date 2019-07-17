"""Completing a data dictionnary with default json schema values
"""
import json
from opentea.fastref import (nob_find,
                             nob_pprint)
from opentea.validation import clean_schema_addresses
# import yaml


def print_dict(dictionary, ident='', braces=1):
    """ Recursively prints nested dictionaries."""

    for key, value in dictionary.items():
        if isinstance(value, dict):
            print('%s- %s' %(ident, key))
            print_dict(value, ident+'  ', braces+1)
        else:
            print(ident+'* %s = %s' %(key, value))


def nob_get_value(obj_, *keys):
    """Retrieve value from nested object given a
    series of keys
    """
    keys_ = list(*keys)
    if keys_:
        _child_obj = obj_[keys_[0]]
        _child_obj = nob_get_value(_child_obj, keys_[1:])
    else:
        _child_obj = obj_
    return _child_obj


def nob_set_value(obj_, value, *keys):
    """set value to nested object given a
    series of keys
    """
    keys_ = list(*keys)
    if keys_:
        key_ = keys_[0]
        del keys_[0]
        if not key_ in obj_:
            obj_[key_] = dict()
        if len(keys_) == 1:
            obj_[key_][keys_[0]] = value
        else:
            nob_set_value(obj_[key_], value, keys_)
    return obj_


def special_case(path):
    """Treating special case in which path
    contains an integer key, this correponds
    to a multiple object carrying a list
    """
    msg = 'Multiple not implemented yet'
    print("%s \n %s : %s \n %s" %(50*'-', msg, path, 50*'-'))


def load_reference_nob(schema):
    """Initialing reference nested object from
    default values and paths given by a json
    schema file

        Parameters
    ----------
    schema_file : Json schema file

    Returns :
    ---------
    schema_ref_paths : paths to object leafs
    data : a nested object containing default values
    """
    schema_paths_list = nob_find(schema, 'default')
    data = dict()
    schema_ref_paths = []
    for path in schema_paths_list:
        value = nob_get_value(schema, path)
        cl_path = clean_schema_addresses(path, ['default'])

        if any(isinstance(key, int) for key in cl_path):
            special_case(cl_path)
        else:
            data = nob_set_value(data, value, cl_path)
            schema_ref_paths.append(cl_path)
    return schema_ref_paths, data


def nob_walk(obj_, pre=None):
    """ Walking recuresively in nested d
    """
    if pre:
        pre = pre[:]
    else:
        pre = []

    if isinstance(obj_, dict):
        for key, value in obj_.items():
            if isinstance(value, dict):
                for d in nob_walk(value, pre+[key]):
                    yield d
            elif isinstance(value, (list, tuple)):
                for v in value:
                    for d in nob_walk(v, pre+[key]):
                        yield d
            else:
                yield pre + [key]
    else:
        yield obj_


def nob_addresses(obj_):
    addresses = list(nob_walk(obj_))
    return addresses


def nob_complete(schema, obj_=dict()):
    """Completing nested object fill up on the basis
    of default reference values given by a schema
    """
    data_obj = obj_.copy()
    ref_paths, ref_obj = load_reference_nob(schema)
    existing_addr = nob_addresses(data_obj)
    for address in ref_paths:
        if not address in existing_addr:
            value = nob_get_value(ref_obj, address)
            nob_set_value(data_obj, value, address)

    return data_obj


def main(schema):
    """ Example of nob_complete usage
    """
    new = nob_complete(schema)

    data_obj = dict()
    data_obj['controle_existif_require'] = dict()
    data_obj['controle_existif_require']['controle'] = dict()
    data_obj['controle_existif_require']['expert_model'] = dict()

    data_obj['controle_existif_require']['controle']['controle_ei'] = True
    data_obj['controle_existif_require']['expert_model']['a1'] = 5.0
    data_obj['controle_existif_require']['expert_model']['a2'] = 6.0
    data_obj['controle_existif_require']['expert_model']['a3'] = 7.0

    data_obj_c = nob_complete(schema, data_obj)

    #print_dict(data_obj)
    # print(nob_pprint(data_obj_c))


if __name__ == "__main__":
    with open('schema.json', "r") as fin:
        SCHEMA = json.load(fin)
    main(SCHEMA)
