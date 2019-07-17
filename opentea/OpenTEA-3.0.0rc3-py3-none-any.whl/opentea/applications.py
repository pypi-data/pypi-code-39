""" module to handle application preparations """

import os


def build_application_dict(ot_path, cfg_dct):
    """ build app dictionary

    Parameters :
    ------------
    ot_path : str, path to opentea sources in use
    cfg_dct : configuration dict

    Returns :
    ---------
    app_dict : dict , with apps as keys, and app paths as values
    app_warn : str , all warnings

    """
    lib_path = os.path.join(ot_path, "library")

    items_in_library = os.listdir(lib_path)
    items_in_cfg = list(cfg_dct["externalApps"].keys())

    app_warn = ""
    # custom file is overraiding library
    intersection = list(set(items_in_library) & set(items_in_cfg))
    if intersection:
        app_warn += ("Some applications in library "
                     "were redefined by custom file: "
                     + ";".join(intersection)
                     + "\n")
    #buiild initial dict
    raw_app_dict = {}
    for item in items_in_library:
        raw_app_dict[item] = os.path.join(lib_path, item)
    for item in items_in_cfg:
        raw_app_dict[item] = cfg_dct["externalApps"][item]

    # remove unsatisfactory apps
    app_dict = {}
    for app in raw_app_dict:
        valid, warn = _app_is_valid(app, raw_app_dict[app])
        if valid:
            app_dict[app] = raw_app_dict[app]
        else:
            app_warn += warn + "\n"

    return app_dict, app_warn


def _app_is_valid(app_name, app_path):
    """ test if an application source has the correct shape

    Parameters :
    ------------
    app_name : str, app_name
    app_path : str , app path

    Returns :
    ---------
    out_bool : boolean, True if valid
    out_warn : str, warning string

    """

    out_bool = True
    out_warn = ""
    if not os.path.isdir(app_path):
        out_warn = app_path + " is not a valid app directory"
        out_bool = False

    if not os.path.isdir(os.path.join(app_path, "XML")):
        out_warn = app_path + " is not a valid app directory (/XML missing)"
        out_bool = False
    if not os.path.isdir(os.path.join(app_path, "scripts")):
        out_warn = (app_path
                    + " is not a valid app directory (/scripts missing)")
        out_bool = False

    if not os.path.isdir(os.path.join(app_path, "XML", app_name)):
        out_warn = (app_path
                    + " is not a valid app directory (/XML/"
                    + app_name
                    + " missing)")

        out_bool = False

    return out_bool, out_warn


def str_app_clusters(app_dict, cfg_dct):
    """ build string from  cluster dict

    Parameters :
    ------------
    app_dict : dict , with apps as keys, and app paths as values
    cfg_dct : configuration dict

    Return :
    --------
    out_str : string showing app clusters

    """
    all_apps = list(app_dict.keys())
    cluster_dict = {}
    for cluster in cfg_dct["customAppClusters"]:
        cluster_dict[cluster] = []
        for app in cfg_dct["customAppClusters"][cluster]:
            if app in all_apps:
                cluster_dict[cluster].append(app)
                all_apps.remove(app)

        cluster_dict["Misc."] = []
        for app in all_apps:
            cluster_dict["Misc."].append(app)

    headers = sorted(cluster_dict.keys())

    max_width = max(len(word) for word
                    in list(app_dict.keys()) + list(cluster_dict.keys()))

    max_rows = max(len(list_) for list_ in list(cluster_dict.values()))

    out_str = ""
    out_str += "\n"
    out_str += "AVAILABLE APPLICATIONS"
    out_str += "\n"
    out_str += ("".join(word.upper().ljust(max_width+2) for word in headers))
    out_str += "\n"
    for i in range(max_rows):
        row = []
        for cluster in headers:
            #print cluster, i , len(cluster_dict[cluster])
            if i < len(cluster_dict[cluster]):
                row.append(cluster_dict[cluster][i])
            else:
                row.append("")
        out_str += ("".join(word.ljust(max_width+2) for word in row))
        out_str += "\n"
    out_str += "\n"

    return out_str
