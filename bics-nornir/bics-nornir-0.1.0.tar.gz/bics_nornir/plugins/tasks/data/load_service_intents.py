import os
from copy import deepcopy

from nornir.core.task import Result, Task

import ruamel.yaml


def load_service_intents(task: Task, directory: str) -> Result:
    """
    Loads intents from intent files
    
    Arguments:

    Examples:

    """
    host_data = {}
    resources_to_populate = set()

    for dirpath, _, files in os.walk(directory):
        for name in files:
            if not name.lower().endswith((".yml", ".yaml")):
                continue
            with open(os.path.join(dirpath, name), "r") as f:
                yml = ruamel.yaml.YAML(typ="safe")
                data = yml.load(f)
            service_hosts = data.get("_service_hosts", [])
            if task.host.name not in service_hosts:
                continue
            service_id = data.get("_service_id", None)
            if not service_id:
                raise ValueError(f"'_service_id' missing in file {name}")
            for rsc in data.pop("_service_required_resources", []):
                resources_to_populate.add(rsc)
            host_params = data.get("host_params", {})
            if task.host.name in host_params:
                data.update(host_params[task.host.name])
            if host_params:
                del (data["host_params"])
            host_data.update({service_id: data})
    task.host["service_intent"] = host_data
    task.host["rsc_to_populate"] = resources_to_populate

    return Result(host=task.host, result=host_data)
