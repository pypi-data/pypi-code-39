import os
from copy import deepcopy

from nornir.core.task import Result, Task

import ruamel.yaml


def load_merge_yaml(task: Task, directory: str) -> Result:
    """
    Loads intents from intent files
    
    Arguments:

    Examples:

    """
    global_data = {}
    group_data = {}
    host_data = {}

    for dirpath, _, files in os.walk(directory):
        for name in files:
            if not name.lower().endswith((".yml", ".yaml")):
                continue
            with open(os.path.join(dirpath, name), "r") as f:
                yml = ruamel.yaml.YAML(typ="safe")
                data = yml.load(f)
            target_scope = data.pop("_target_scope", "")
            target_groups = data.pop("_target_groups", [])
            target_host = data.pop("_target_host", "")
            if "_path" in data:
                path = data["_path"]
                data = {path: data}
            if target_scope.upper() == "GLOBAL":
                _merge(global_data, data)
            elif target_scope.upper() == "GROUP":
                for group in target_groups:
                    if task.host.has_parent_group(group):
                        _merge(group_data, data)
            elif target_scope.upper() == "HOST":
                if target_host == task.host.name:
                    _merge(host_data, data)

    _merge(group_data, global_data)
    _merge(host_data, group_data)

    return Result(host=task.host, result=host_data)


def _merge(a, b):
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                _merge(a[key], b[key])
            else:
                pass  # a always wins
        else:
            a[key] = b[key]
