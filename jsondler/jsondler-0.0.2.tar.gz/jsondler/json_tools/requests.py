import operator
from collections import Mapping
from functools import reduce


def get_by_path(in_json, path_list, prefix_list=None):
    pairs_list = list()
    if type(in_json) not in (dict, list, tuple):
        return pairs_list
    if prefix_list is None:
        prefix_list = list()
    if len(path_list) == 1:
        if path_list[0] == "*":
            if type(in_json) is dict:
                for key in in_json:
                    pairs_list.append((prefix_list.__add__([key]), in_json[key]))
            else:
                for i in range(len(in_json)):
                    pairs_list.append((prefix_list.__add__([i]), in_json[i]))
        elif type(path_list[0]) in (list, tuple, set, frozenset):
            for path_part in path_list[0]:
                try:
                    pairs_list.append((prefix_list.__add__([path_part]), in_json[path_part]))
                except (KeyError, TypeError):
                    pass
        else:
            try:
                pairs_list = [(prefix_list.__add__([path_list[0]]), in_json[path_list[0]])]
            except (KeyError, IndexError, TypeError):
                pass
    elif len(path_list) > 1:
        if path_list[0] == "*":
            if type(in_json) is dict:
                for key in in_json:
                    pairs_list.__iadd__(get_by_path(in_json[key], path_list[1:], prefix_list.__add__([key])))
            else:
                for i in range(len(in_json)):
                    pairs_list.__iadd__(get_by_path(in_json[i], path_list[1:], prefix_list.__add__([i])))
        elif type(path_list[0]) in (list, tuple, set, frozenset):
            for path_part in path_list[0]:
                try:
                    pairs_list.__iadd__(get_by_path(in_json[path_part], path_list[1:],
                                                    prefix_list.__add__([path_part])))
                except (KeyError, TypeError):
                    pass
        else:
            try:
                pairs_list = get_by_path(in_json[path_list[0]], path_list[1:],
                                         prefix_list.__add__([path_list[0]]))
            except (KeyError, TypeError):
                pass
    return pairs_list


def deepupdate(d, u):
    if d is None:
        d = dict()
    if u is None:
        u = dict()
    for k, v in u.items():
        if isinstance(v, Mapping):
            d[k] = deepupdate(d.get(k, dict()), v)
        else:
            d[k] = v
    return d


def deepdiff(d1, d2):
    """
    Calculates the minimal dict that need to be the input as u to deepupdate to get d2 from d1
    :param d1: dict 1
    :param d2: dict 2
    :return: dict
    """
    diff_dict = dict()
    k1_set = set()

    for k1 in d1:
        if k1 in d2:
            if d1[k1] != d2[k1]:
                if type(d1[k1]) is dict and type(d2[k1]) is dict:
                    diff_dict_k1 = deepdiff(d1=d1[k1], d2=d2[k1])
                    if diff_dict_k1:
                        diff_dict[k1] = diff_dict_k1
                else:
                    diff_dict[k1] = d2[k1]
        else:
            diff_dict[k1] = None
        k1_set.add(k1)

    for k2 in d2:
        if k2 not in k1_set:
            diff_dict[k2] = d2[k2]

    return diff_dict


def tuplize_json_coord_pairs(in_dict, *json_paths):
    for json_path in json_paths:
        for pair in get_by_path(in_dict, json_path):
            if len(pair) == 2 and pair[1]:
                reduce(operator.getitem, pair[0][:-1], in_dict)[pair[0][-1]] = tuple(pair[1])
    return in_dict


def query(in_json, condition_list, condition_tree="AND"):
    """

    :param in_json: dict or list
    :param condition_list: list of conditions with items (path_list, lambda x: True condition)
    :param condition_tree: conditions tree from condition_list that define True or False for got entries
    :return: list of pairs (path_list, value) for which condition_tree is True
    """
    return


def where(in_json, path_list, condition):
    pairs_list = list()
    for json_path, value in get_by_path(in_json=in_json, path_list=path_list):
        if condition(value):
            pairs_list.append((json_path, value))
    return pairs_list
