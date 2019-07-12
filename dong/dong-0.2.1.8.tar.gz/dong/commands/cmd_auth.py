import click

import dong
import dong.auth


@click.group()
def auth():
    """auth ."""
    pass


@auth.command(help='Authentication related functions.')
def status():
    netrc = dong.auth.load_netrc()
    print(netrc[dong.SERVER_NAME]['login'])


@auth.command(help='Login with your credentials.')
@click.option('-u', '--username', prompt=True)
@click.option('-p', '--password', prompt=True, hide_input=True)
def login(username, password):
    print("U: {} P: {}".format(username, password))
