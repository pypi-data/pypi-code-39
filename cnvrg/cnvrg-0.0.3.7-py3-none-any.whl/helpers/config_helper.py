import os
import yaml

CONFIG_TYPE_PROJECT = "PROJECT"
CONFIG_TYPE_DATASET = "DATASET"

def find_config_dir(path=None):
    currdir = path or os.curdir
    while os.path.realpath(currdir) != os.path.expanduser("~") and os.path.realpath(currdir) != "/":
        if os.path.exists(os.path.join(currdir, '.cnvrg', 'config.yml')):
            return currdir
        currdir = os.path.join(currdir, '..')
    return False

def config_path(path=None):
    config_dir = find_config_dir(path=path)
    return os.path.join(config_dir, ".cnvrg", "config.yml")

def load_config(path=None):
    with open(config_path(path), 'r') as f:
        return yaml.safe_load(f)

def config_type(path=None):
    if not find_config_dir(path):
        return None
    config = load_config(path=path)
    if "project" in config or ":project_name" in config:
        return CONFIG_TYPE_PROJECT
    return CONFIG_TYPE_DATASET


def save_config(config, path=None):
    config_dir = find_config_dir(path=path)
    config_dir = os.path.join(config_dir or path, ".cnvrg")
    os.makedirs(config_dir, exist_ok=True)
    config_path = os.path.join(config_dir, "config.yml")
    with open(config_path, "w+") as f:
        yaml.dump(config, f)

def is_in_dir(dir_type, dir_element, working_dir):
    if not find_config_dir(working_dir): return False
    if not config_type(working_dir) == dir_type: return False
    config = load_config(working_dir)
    return config.get(":project_name") or config.get("project_name") or config.get(":dataset_name") or config.get("dataset_name") == dir_element



