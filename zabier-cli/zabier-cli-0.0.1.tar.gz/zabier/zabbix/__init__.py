from __future__ import annotations

from zabier.zabbix.hostgroup import HostGroupMixin

zabbix = None

class Zabbix(HostGroupMixin):
    pass


def configure(url: str, user_name: str, password: str):
    global zabbix
    zabbix = Zabbix(
        url = url,
        user_name = user_name,
        password = password)


def get_client():
    global zabbix
    if zabbix is None:
        raise Exception('Zabbix client is not configured.')
    zabbix.login()
    return zabbix
