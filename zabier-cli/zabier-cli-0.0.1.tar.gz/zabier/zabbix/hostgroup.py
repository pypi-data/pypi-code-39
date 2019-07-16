from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional, List

from zabier.zabbix.base import ZabbixBase


@dataclass
class HostGroup:
    groupid: str


class HostGroupMixin(ZabbixBase):
    def create_host_group(self, host_group_name: str):
        ret = self.do_request(
            "hostgroup.create",
            {'name': host_group_name}
        )
        return HostGroup(groupid=ret['result']['groupids'].pop())

    def host_group_exists(self, host_group_name) -> bool:
        response: Dict = self.do_request(
            "hostgroup.get",
            {
                    "countOutput": 'true',
                    "search": {
                        "name": [host_group_name]
                    },
                    "editable": True,
                    "startSearch": True,
                    "searchByAny": True
            }
        )
        return int(response['result']) > 0

