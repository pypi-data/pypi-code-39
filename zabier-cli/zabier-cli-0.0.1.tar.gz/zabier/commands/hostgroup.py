import click

from zabier.zabbix import get_client

def create_hostgroup(name: str):
    zabbix = get_client()
    if zabbix.host_group_exists(name):
        click.echo('Host group "{}" already exists.'.format(name))
    else:
        hostgroup = zabbix.create_host_group(name)
        click.echo('Host group created. ID: {}'.format(hostgroup.groupid))
