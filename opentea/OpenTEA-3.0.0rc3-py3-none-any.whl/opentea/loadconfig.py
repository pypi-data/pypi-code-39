""" Module to read the config file of opentea"""
import os
import configparser


OT_CONFIG_SECTIONS = ["openteaConfiguration",
                      "localEnvironmentVariables",
                      "openteaCustomAppearance",
                      "externalApps",
                      "customAppClusters"]


def _minimum_config():
    """ set the minimal config
    could become a json.

    Returns :
    ---------
    conf_d : dict, config params with minimal requirements

    """
    conf_d = {}

    for section in OT_CONFIG_SECTIONS:
        conf_d[section] = {}

    section = "openteaCustomAppearance"
    conf_d[section] = {}
    conf_d[section]["focusCorrection"] = 0
    conf_d[section]["guiHeight"] = 800
    conf_d[section]["guiWidth"] = 400
    conf_d[section]["pythonExec"] = "/usr/bin/env python"
    conf_d[section]["themeTk"] = "clam"
    conf_d[section]["autoSave"] = 1
    conf_d[section]["balloonOnOff"] = 0
    return conf_d


def _load_config_raw(configfile):
    """ load the config file of opentea

    Parameters :
    ------------
    configfile : str, path to a config ini file

    Returns :
    ---------
    conf_d : dict, config params

    """
    config = configparser.ConfigParser()

    # to avoid lower casing conversion
    config.optionxform = str
    config.read_file(open(configfile))
    conf_d = _minimum_config()

    # mandatory values
    section = "openteaConfiguration"
    for item in ["configPath",
                 "pluginsPath"]:
        conf_d[section][item] = config.get(section, item)

    # optional values
    for section in ["localEnvironmentVariables",
                    "openteaCustomAppearance",
                    "externalApps",
                    "customAppClusters"]:
        for pairs in config.items(section):
            conf_d[section][pairs[0]] = pairs[1]
    return conf_d


def _expand_vars_config(conf_d):
    """ expand environement variables

    Parameters :
    ------------
    conf_d : dict, config params

    Returns :
    ---------
    out_c : dict, config params

    """

    out_c = dict(conf_d)
    for section in ["localEnvironmentVariables",
                    "openteaConfiguration",
                    "externalApps"]:
        for item in conf_d[section]:
            out_c[section][item] = os.path.expandvars(conf_d[section][item])
    return out_c


def _clusters_to_list(conf_d):
    """ move cluster values to lists

    Parameters :
    ------------
    conf_d : dict, config params

    Returns :
    ---------
    out_c : dict, config params

    """
    out_c = dict(conf_d)
    for cluster in conf_d["customAppClusters"]:
        out_c["customAppClusters"][cluster] = [
            item.strip('\"')
            for item in conf_d["customAppClusters"][cluster].split()]
    return out_c


def _update_environement(conf_d):
    """ update environement variables for this process

    Parameters :
    ------------
    conf_d : dict, config params

    Effect :
    --------
    NOT STATELESS
    os.environ updated

    """
    section = "localEnvironmentVariables"
    for var in conf_d[section]:
        os.environ[var] = conf_d[section][var]


def str_config(cfg):
    """ string representing the config file

    Parameters :
    ------------
    cfg : dict, config params

    Returns :
    ---------
    out_str : str, show configuration

    """
    out_str = ""
    for item in cfg:
        out_str += item + "\n"
        for subitem in cfg[item]:
            out_str += ("   |"
                        + subitem
                        + " : "
                        + str(cfg[item][subitem])
                        + "\n")
    return out_str


def load_config(fin):
    """ main load config

    Parameters :
    ------------
    fin : str, pathto config .ini file

    Returns :
    ---------
    cfg : dict, config params

    """
    cfg = _load_config_raw(fin)
    _update_environement(cfg)
    cfg = _expand_vars_config(cfg)
    cfg = _clusters_to_list(cfg)
    return cfg
