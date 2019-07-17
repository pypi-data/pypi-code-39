"""Module to operate a trplie layer of validation"""


import json
import jsonschema

from opentea.fastref import (nob_find,
                             nob_find_unique,
                             nob_node_exist,
                             nob_get, 
                             nob_pprint)

class ValidationErrorShort(Exception):
    pass

def validate_schema(data, schema):
    """Scjema validation procedure.

    Parameters:
    -----------
    data : a nested dict to validate
    schema : the schema to validate against (jsonschema grammar)

    Return:
    -------
    Only exceptions are returned if any problem"""  

    # too verbose to be of use
    #jsonschema.validate(data, schema)

    validator = jsonschema.Draft4Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)

    err_msg = ""
    if errors:
        for error in errors:
            err_msg += "\n" + error.message + "\n"
            err_msg += nob_pprint(error.schema, max_lvl=4)

        raise ValidationErrorShort(err_msg)

    return 

class ValidationErrorExistIf(Exception):
    pass

def validate_existifs(data, schema):
    """Validate existif dependencies.

    if an item existence depends on the value of one other item

    Parameters :
    -----------
    data : a nested dict to validate
    schema : the schema to validate against (jsonschema grammar)

    Return:
    -------
    Only exceptions are returned if any problem"""

    for sch_address in nob_find(schema, "existif"):
        condition = nob_get(schema, *sch_address)
        dat_address = clean_schema_addresses(sch_address[:-1])
        if nob_node_exist(data, *dat_address):
            if not nob_node_exist(data, condition["node"]):
                msgerr = ("node -" + "/".join(dat_address)
                          + "- cannot exist if a condition node -"
                          + condition["node"]
                          + "- is not present.")
                raise ValidationErrorExistIf(msgerr)
            else:
                outcome = None
                value = nob_get(data, condition["node"])
                if isinstance(value, (int, float)):
                    if condition["operator"] == "==":
                        outcome = value == condition["value"]
                    elif condition["operator"] == ">=":
                        outcome = value >= condition["value"]
                    elif condition["operator"] == "<=":
                        outcome = value <= condition["value"]
                    elif condition["operator"] == ">":
                        outcome = value > condition["value"]
                    elif condition["operator"] == "<":
                        outcome = value < condition["value"]
                    elif condition["operator"] != "!=":
                        outcome = value != condition["value"]
                    else:
                        raise NotImplementedError(
                            "operator :" + condition["operator"])

                if isinstance(value, (bool)):
                    if condition["operator"] == "==":
                        outcome = value is condition["value"]
                    elif condition["operator"] == "!=":
                        outcome = value is not condition["value"]
                    else:
                        raise NotImplementedError(
                            "operator :" + condition["operator"])

                if outcome is False:
                    msgerr = ("node " + "/".join(dat_address)
                              + "do no pass test :"
                              + condition["node"]
                              + str(condition["operator"])
                              + str(condition["value"]))
                    raise ValidationErrorExistIf(msgerr)


class ValidationErrorRequire(Exception):
    pass

def validate_require(data, schema):
    """Validate require dependencies.

    if  children of an item depends of the value of one other item

    Parameters :
    -----------
    data : a nested dict to validate
    schema : the schema to validate against (jsonschema grammar)

    Return:
    -------
    Only exceptions are returned if any problem"""

    for req_address in nob_find(schema, "require"):
        src_key = nob_get(schema, *req_address)
        dst_address = clean_schema_addresses(req_address[:-1])
        #dst_node = nob_get(schema, *dst_address)
        print("\nResolving require for", "/".join(dst_address))
        print(" using dependance from ", src_key)

        if nob_node_exist(data, *dst_address):
            print("Node exist in data, testing...")
            if not nob_node_exist(data, src_key):
                msgerr = ("node children-" + "/".join(dst_address)
                          + "- cannot exist if a require node -"
                          + src_key
                          + "- is not present.")
                raise ValidationErrorRequire(msgerr)
            else:
                src_keys = set(nob_get(data, src_key))
                dst_object = nob_get(data, *dst_address)
                if isinstance(dst_object, list):
                    if isinstance(dst_object[0] , str):
                        dst_keys = set(dst_object)
                    elif isinstance(dst_object[0] , dict):
                        dst_keys_list = []
                        for dict_item in dst_object:
                            if "name" in dict_item:
                                dst_keys_list.append(dict_item["name"])
                            else:
                                msgerr = ("attribute name is missing for item " +
                                    nob_pprint(dict_item))
                                raise ValidationErrorRequire(msgerr)

                        dst_keys = set(dst_keys_list)

                if src_keys == dst_keys:
                    print("Require succesfull")
                else:
                    msgerr = ("object " + "/".join(dst_address) +
                              " children are [" + ", ".join(dst_keys)) + "]"
                    msgerr += ("\nmismatch with require  " + src_key +
                               " : [" + ", ".join(src_keys)) + "]"
                    raise ValidationErrorRequire(msgerr)


def clean_schema_addresses(list_, udf_stages=None):
    """Clean a address from the addtitionnal layers of SCHEMA.

    Used only when a SCHEMA address must be found in the data to validate

     Parameters :
    -----------
    list_ : a list of string
        address in a nested dict
    udf_stages : a list of additionnal user defined stages (udf)
    Returns :
    ---------
    list
        the same list without SCHEMA intermedaite stages
    """
    skipped_stages = ["properties", "oneOf"]
    if udf_stages is not None:
        for udf_stage in udf_stages:
            skipped_stages.append(udf_stage)
    out = []
    for item in list_:
        if item not in skipped_stages:
            out.append(item)
    return out


def main_validate(data, schema):
    """Main validation procedure.

    Parameters:
    -----------
    data : a nested dict to validate
    schema : the schema to validate agains (jsonschema grammar)

    Return:
    -------
    Only exceptions are returned if any problem"""

    validate_schema(data, schema)
    validate_existifs(data, schema)
    validate_require(data, schema)

if __name__ == "__main__":
    with open("./schema.json", "r") as fin:
        SCH = json.load(fin)
    with open("./test.json", "r") as fin:
        DAT = json.load(fin)

    main_validate(DAT, SCH)
