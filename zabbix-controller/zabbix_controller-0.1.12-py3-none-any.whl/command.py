from .utils import *


@click.group(help=('Entry point.\n'
                   'Initialize ZabbixAPI.')
             )
@click.option('-aa', '--apiserver-address', default='http://localhost:8081',
              help=('Zabbix api server address.\n'
                    'ex) http://localhost:8081')
              )
@click.option('-u', '--username', default='Admin', help='Zabbix username')
@click.option('-p', '--password', default='zabbix', help='Zabbix password')
@click.option('-bu', '--basicauth-username', default=None, help='Basic authentication username')
@click.option('-bp', '--basicauth-password', default=None, help='Basic authentication password')
@click.option('--dry-run', default=False, is_flag=True,
              help=('Activate debug mode.\n'
                    'Create, Update, Delete API are not executed.\n'
                    'Only Get API is executed.'))
@click.option('-i', '--interactive', default=False, is_flag=True,
              help=('Turn on interactive mode.\n'
                    'Confirmation is still available.'))
@click.pass_context
def main(
        ctx,
        apiserver_address,
        username, password,
        basicauth_username, basicauth_password,
        dry_run,
        interactive,
):
    """
    entry point
    """
    # stream = logging.StreamHandler(sys.stdout)
    # stream.setLevel(logging.DEBUG)
    # log = logging.getLogger('pyzabbix')
    # log.addHandler(stream)
    # log.setLevel(logging.DEBUG)

    zapi = zabbix_auth(apiserver_address, username, password, basicauth_username, basicauth_password)
    ctx.obj = ZabbixCTL(zapi, dry_run=dry_run, interactive=interactive)
