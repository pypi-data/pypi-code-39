from collections import OrderedDict

from jsondler.json_tools.requests import get_by_path


def index_dicts_list(in_dicts_list, by, path=False):
    indexed_data = OrderedDict()
    if not path:
        for elm in in_dicts_list:
            if elm[by] in indexed_data.keys():
                indexed_data[elm[by]].append(elm)
            else:
                indexed_data[elm[by]] = [elm]
    else:
        got_by_path = get_by_path(in_json=in_dicts_list, path_list=by)
        for got_pair in got_by_path:
            if got_pair[1] in indexed_data.keys():
                indexed_data[got_pair[1]].append(in_dicts_list[got_pair[0][0]])
            else:
                indexed_data[got_pair[1]] = [in_dicts_list[got_pair[0][0]]]
    return indexed_data
