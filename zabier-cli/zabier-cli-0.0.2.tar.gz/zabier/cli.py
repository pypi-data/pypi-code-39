import os

import click

from zabier.commands.hostgroup import create_hostgroup
from zabier.zabbix import configure, zabbix

@click.group(invoke_without_command=True)
@click.option('-H', '--host',
    required=False, type=str,
    default=os.environ.get('ZABBIX_HOST', ''))
@click.option('-u', '--user',
    required=False,
    type=str,
    default=os.environ.get('ZABBIX_USER', ''))
@click.option('-p', '--password',
    required=False,
    type=str,
    default=os.environ.get('ZABBIX_PASSWORD', ''))
@click.pass_context
def main(ctx: click.Context, host: str, user: str, password: str):
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
    else:
        configure(host, user, password)


@main.command(help='Apply the host group')
@click.option('-n', '--name', required=True, type=str)
def hostgroup(name: str):
    create_hostgroup(name)
