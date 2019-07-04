from nornir.core.task import Result, Task

from bics_nornir.plugins.tasks.networking import nc


def eline(task: Task, **kwargs):
    service_id = kwargs.pop("_service_id")
    service_hosts = kwargs.pop("_service_hosts")
    service_type = kwargs.pop("_service_type")
    operation = kwargs.pop("_service_operation")

    data = {}
    data.update(kwargs)
    data["service_id"] = service_id

    if operation.lower() == "replace":
        data["operation"] = "replace"
        other_host = ""
        for h in service_hosts:
            if h not in task.host.name:
                other_host = h
                break
        saps = kwargs.get("saps")
        local_epipe = False
        if isinstance(saps, list):
            if len(saps) == 2:  # local epipe
                local_epipe = True
        else:
            raise ValueError(f"saps must be a list")
        if not local_epipe:
            if not other_host:
                raise Exception(f"Eline {service_id} has not remote host")
            other_sys_ip = task.nornir.inventory.hosts[other_host]["config"].get(
                "/router/router-name=Base/interface/interface-name=system", {}
            )
            if not other_sys_ip:
                raise Exception(f"Cannot get system-ip for {other_host} from inventory")
            other_sys_ip = other_sys_ip["ipv4"]["primary"]["address"]

            sdp_info = task.host["config"].get("/service/sdp", {})
            sdp_id = ""
            if sdp_info.get("_count", None):  # multiple sdp's
                for seq, attrs in sdp_info.items():
                    if str(seq).startswith("_"):
                        continue
                    if attrs.get("far-end", {}).get("ip-address", "") == other_sys_ip:
                        sdp_id = attrs.get("sdp-id")
                        break
            else:
                sdp_id = sdp_info.get("sdp-id", "")
            if not sdp_id:
                raise Exception(f"Cannot find appropriate SDP to {other_sys_ip}")
            data["sdp_id"] = sdp_id
    elif operation.lower() == "delete":
        data["operation"] = "delete"
    else:
        raise Exception(f"unknown action {operation}")

    return Result(host=task.host, result=data)
