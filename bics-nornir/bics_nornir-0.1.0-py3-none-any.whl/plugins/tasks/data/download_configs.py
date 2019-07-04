from nornir.core.task import Result, Task
from bics_nornir.plugins.tasks.networking import nc


def download_configs(task: Task, resources: set) -> None:
    """
    Loads configs from device to inventory
    
    Arguments:
    resources: list of resource paths to load

    Examples:

    """
    config = {}
    for rsc_path in resources:
        r = task.run(
            name=f"Get {rsc_path}",
            task=nc.get_config,
            source=nc.NcDatastore.running,
            path=rsc_path,
        )
        config.update({rsc_path: r.result})

    task.host["config"] = config
