from collections import defaultdict

import numpy as np


def columnize_dicts_list(dicts_list, na=np.nan):
    col_names = list()
    cols_dict = defaultdict(list)
    d_i = 0
    for dict_i in dicts_list:
        for col_name in col_names:
            cols_dict[col_name].append(dict_i.pop(col_name, np.nan))
        for key in dict_i:
            col_names.append(key)
            cols_dict[key] = [na]*d_i + [dict_i[key]]
        d_i += 1
    return cols_dict
