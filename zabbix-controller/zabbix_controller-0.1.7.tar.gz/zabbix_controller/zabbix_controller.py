import sys
import os
import logging
from pprint import pprint
import re
import time

from pyzabbix import ZabbixAPI
from bullet import Bullet, Check, YesNo
import click

from .utils import *

class Zabbix(object):
    def __init__(self, zapi):
        self.zapi = zapi

@click.group()
@click.option('-aa', '--apiserver-address', default='http://localhost:8081',
              help=('Zabbix api server address.\n'
                    'ex) http://localhost:8081')
              )
@click.option('-u', '--username', default='Admin', help='Zabbix username')
@click.option('-p', '--password', default='zabbix', help='Zabbix password')
@click.option('-bu', '--basicauth-username', default=None, help='Basic authentication username')
@click.option('-bp', '--basicauth-password', default=None, help='Basic authentication password')
@click.pass_context
def main(
    ctx,
    apiserver_address,
    username, password,
    basicauth_username, basicauth_password,
):
    '''
    entry point
    '''
    # stream = logging.StreamHandler(sys.stdout)
    # stream.setLevel(logging.DEBUG)
    # log = logging.getLogger('pyzabbix')
    # log.addHandler(stream)
    # log.setLevel(logging.DEBUG)

    zapi = zabbix_auth(apiserver_address, username, password, basicauth_username, basicauth_password)
    ctx.obj = Zabbix(zapi)

    # TODO: 本当は，gcpのインスタンスがあるかどうかのチェックをする
    # TODO: zabbixにあるhostidとかhostnameと比較して，集合の差をとる (zabbix.hostname - gcp.instancename)
