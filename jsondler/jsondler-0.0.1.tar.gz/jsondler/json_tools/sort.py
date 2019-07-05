import itertools

from jsondler.json_tools import get_by_path


def sort_dicts_list(in_json, prior_list, reverse=False):
    paths_order = get_paths_order(in_json=in_json, prior_list=prior_list, reverse=reverse)
    out_json = list()
    for path in paths_order:
        out_json.append(in_json[path[0]])
    [in_json.pop(path[0]) for path in sorted(paths_order, key=lambda p: p[0], reverse=True)]
    out_json.__iadd__(in_json)
    return out_json


def get_paths_order(in_json, prior_list, reverse=False, preorder=None):
    # returns list of paths (no regular expressions): [path_1, path_2, ..., path_n]
    paths_order = list()
    if preorder is None:
        curr_lev = sorted(get_by_path(in_json=in_json, path_list=prior_list[0]), key=lambda p: p[1], reverse=reverse)
        if len(prior_list) == 1:
            return list(map(lambda p: p[0], curr_lev))
        return get_paths_order(in_json=in_json,
                               prior_list=prior_list[1:],
                               reverse=reverse,
                               preorder=_group_by_value(curr_lev))

    for group in preorder:
        paths_to_get = _superpos_paths(real_paths=group, path_to_superpos=prior_list[0])
        curr_lev = sorted(itertools.chain.from_iterable(map(lambda path: get_by_path(in_json=in_json,
                                                                                     path_list=path),
                                                            paths_to_get)),
                          key=lambda p: p[1], reverse=reverse)
        if len(prior_list) == 1:
            paths_order.__iadd__(map(lambda p: tuple(p[0]), curr_lev))
        else:
            paths_order.__iadd__(get_paths_order(in_json=in_json,
                                                 prior_list=prior_list[1:],
                                                 reverse=reverse,
                                                 preorder=_group_by_value(curr_lev)))
    return paths_order


def _group_by_value(sorted_items):
    v = None
    groups_list = list()
    group_list = list()
    for item in sorted_items:
        if item[1] != v:
            if group_list:
                groups_list.append(group_list.copy())
            group_list = [item[0]]
            v = item[1]
        else:
            group_list.append(item[0])
    groups_list.append(group_list.copy())
    return groups_list


def _superpos_paths(real_paths, path_to_superpos):
    superposed_paths = [[[], True] for i in range(len(real_paths))]
    for i in range(len(path_to_superpos)):
        for j in range(len(real_paths)):
            if not superposed_paths[j][1]:
                continue
            if path_to_superpos[i] == "*":
                try:
                    superposed_paths[j][0].append(real_paths[j][i])
                except IndexError:
                    superposed_paths[j][1] = False
                    superposed_paths[j][0].__iadd__(path_to_superpos[i:])
            elif type(path_to_superpos[i]) in (list, tuple, set, frozenset):
                try:
                    if real_paths[j][i] in path_to_superpos[i]:
                        superposed_paths[j][0].append(real_paths[j][i])
                    else:
                        superposed_paths[j][1] = False
                        superposed_paths[j][0].__iadd__(path_to_superpos[i:])
                except IndexError:
                    superposed_paths[j][1] = False
                    superposed_paths[j][0].__iadd__(path_to_superpos[i:])
            else:
                try:
                    if real_paths[j][i] == path_to_superpos[i]:
                        superposed_paths[j][0].append(real_paths[j][i])
                    else:
                        superposed_paths[j][1] = False
                        superposed_paths[j][0].__iadd__(path_to_superpos[i:])
                except IndexError:
                    superposed_paths[j][1] = False
                    superposed_paths[j][0].__iadd__(path_to_superpos[i:])
    return set(map(lambda p: tuple(p[0]), superposed_paths))
