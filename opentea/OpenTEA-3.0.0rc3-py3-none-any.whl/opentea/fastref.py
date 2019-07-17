"""Nested object services.

A nested object is here: 
 -nested dicts
 -nested lists
 -a mix of nested lists and nested dicts

An address is a list of strings and/or integers 
giving a position in the nested object

Hereafter, the -address, complete or not- statement
refer to an address with potentially missing elements.

EXAMPLE:@
for a dict such as :
d["a"]["b"]["c"]["d"]["e"]["f"]
this the full address 
[ ["a","b","c","d","e"] ]
can be found  with either:
nob_find(d, "a","b","c","d","e") (full path)
nob_find(d, "b","d","e") (partial path)
nob_find(d, "e") (only one hint )


"""

import yaml

def nob_get(obj_, *keys):
    """Retrun an object from a nested object

    Parameters
    ----------
    obj_ : nested object
    keys : address, complete or not

    Returns
    -------
    object : the object found at this address
    """
    address = nob_find_unique(obj_, *keys)
    tmp = obj_.copy()
    for key in address:
        tmp = tmp[key]
    return tmp


def nob_node_exist(obj_, *keys):
    """ Test if one node exist in a nested object

    Parameters
    ----------
    obj_ : nested object
    keys : address, complete or not

    Returns :
    ---------
    boolean
    """
    try:
        found_addr = nob_find_unique(obj_, *keys)
    except RuntimeError:
        return False
    return True


def nob_find_unique(obj_, *keys):
    """Find a unique occurences of a key in a nested object.
    Raise exceptions if problems

    Parameters
    ----------
    obj_ : nested object
    keys : address, complete or not

    Returns :
    ---------
    one single address matching the input address
    """
    matchlist = nob_find(obj_, *keys)
    keys_str = " ".join([str(key) for key in [*keys]])
    if not matchlist:
        raise RuntimeError("No match for keys -" + keys_str + "-")
    elif len(matchlist) > 1:
        match_err = ["/".join(match) for match in matchlist]
        raise RuntimeError("Multiple match for key -" + keys_str + "-"
                           + "\n".join(match_err))
    else:
        return matchlist[0]


def nob_find(obj_, *keys):
    """Find all occurences matching a serie of keys in a nested object.

    Parameters
    ----------
    obj_ : nested object
    keys : address, complete or not

    Returns :
    ---------
    list of addresses matching the input address
    """
    if not keys:
        raise RuntimeError("No key provided..")
    target_key = keys[-1]
    matching_addresses = []

    def rec_findkey(obj_, target_key, path):
        if isinstance(obj_, dict):
            for key in obj_:
                if key == target_key:
                    matching_addresses.append(path + [key])
                rec_findkey(obj_[key], target_key, path + [key])
        if isinstance(obj_, list):
            for key, item in enumerate(obj_):
                if isinstance(item, dict):
                    if "name" in item:
                        if key == item["name"]:
                            matching_addresses.append(path + [key])
                rec_findkey(item, target_key, path + [key])

    rec_findkey(obj_, target_key, [])

    out = []
    for addr in matching_addresses:
        if all([clue in addr for clue in keys[:-1]]):
            out.append(addr)
    return out


def nob_pprint(obj_, max_lvl=None):
    """ return a pretty print of a nested object.
    yaml.dump() in use for the display

    Parameters :
    ------------
    obj_ : nested object
    max_lvel : optional :  maximum nber of levels to show

    Output :
    --------
    out : string showing the nested_object structure
    """
    yamlstr = None
    if max_lvl is None:
        yamlstr = yaml.dump(obj_, default_flow_style=False)

    else:
        def rec_copy(obj_, lvl):
            out = None
            if lvl == 0:
                out = "(...)"
            else:
                if isinstance(obj_, dict):
                    out = {}
                    for key in obj_:
                        out[key] = rec_copy(obj_[key], lvl-1)
                elif isinstance(obj_, list):
                    out = []
                    for elmt in obj_:
                        out.append(rec_copy(elmt, lvl-1))
                else:
                    out = obj_
            return out

        out = rec_copy(obj_, max_lvl)
        yamlstr = yaml.dump(out, default_flow_style=False)

    return yamlstr


# def flatten_dict(dict_, search_key, parent_key="", sep="/"):
#     """Search recursively the keyword search_key in input dict.
#        Create key with path using separators
#        The value assigned to the key is the child of search_key in input dict

#     Parameters
#     ----------
#     dict_ : dict
#         Input dictionary
#     search_key : string
#         String that corresponds to a key in the input dictionary
#     parent_key : str, optional
#         Contains the key that grows larger when recursively navigating through
#         the nested dictionary (the default is "",
#         which is empty for keys in first dict_ entry)
#     sep : str, optional
#         Separator for the path in key (the default is "/")

#     Returns
#     -------
#     dict
#         Dictionary containing flattened path to nested
#         searched key and value of the original dictionary
#     """
#     search_key_items = []
#     for key, val in dict_.items():
#         new_key = parent_key + sep + key if parent_key else key
#         if isinstance(val, dict):
#             search_key_items.extend(
#                 flatten_dict(
#                     val, search_key, parent_key=new_key, sep=sep
#                 ).items()
#             )
#         else:
#             if search_key == key:
#                 search_key_items.append((new_key, val))
#     return dict(search_key_items)


# def list_to_nested_dict(maplist, target_key, dict_=None):
#     """Create nested dictionary from list and add dict to lowest level.

#     Example output:
#     out_dict[maplist[0]: {maplist[1]: ... {dict_[target_key]}}]         

#     Parameters
#     ----------
#     maplist : list
#         List containing path to object
#     target_key : set
#         Unique keys of dictionary to be assigned to lowest level dict
#     dict_ : dict
#         dictionary to be added if any

#     Returns
#     -------
#     out_dict: dict
#         Nested dictionary created from list
#     """
#     if dict_:
#         out_dict = {
#             str(item): dict_[str(item)]
#             for item in target_key
#             if dict_.get(str(item)) is not None
#         }
#     else:
#         out_dict = {}
#     for key in reversed(maplist[:-1]):
#         int_dict = copy.deepcopy(out_dict)
#         out_dict = {}
#         out_dict[key] = int_dict
#     return out_dict