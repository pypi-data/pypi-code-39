# TODO: フィルターの際に時間で指定できるようにする．hostしか時間はわからなそう
'''
別ファイルに分けるとclickがおかしくなったのでコマンド系は1つのファイルにまとめた
'''
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

pprint(sys.argv)

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
    すべてのコマンドのエントリーポイント
    zapiの設定をする
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

@main.group(help='hosts command')
@click.option('-m', '--match', 
              callback=validate_match,
              help=('For search host by regex. Using re.search() in python. \n'
                    'key:pattern\n'
                    'ex1) name:^some -> This matches some, some-host, ...\n'
                    'ex2) hostid:41 -> This matches 4123232, 111141, ...'
                    'ex3) name:^$ -> This matches empty string')
              )
@click.option('-tm', '--time-match',
              callback=validate_time_match,
              help=('For search time pattern. Using unixtime\n'
                    'key:[from]-[to].\n'
                    'If you use --match at the same time, these mean and operator'
                    'From must be less than to.\n'
                    'ex1) errors_from:48120471-14834017 -> 48120471~14834017\n'
                    'ex2) errors_from:- -> 0~[now unixtime]\n'
                    'ex3) disable_until:-7184 -> 0~7184\n')
              )
@click.pass_obj
def hosts(obj, match, time_match):
    '''
    hostsコマンドのエントリーポイント
    '''
    pprint(match)
    hosts = get_hosts(obj.zapi, match=match, time_match=time_match)

    if len(hosts) == 0:
        print('There is no host')
        exit(0) 

    obj.hosts = hosts

@hosts.command(help='list hosts')
@click.pass_obj
def list(obj):
    '''
    hostsをリストする
    '''
    click.echo(obj.hosts)

    
@hosts.command(help='delete hosts')
@click.pass_obj
def delete(obj):
    '''
    hostを削除する
    '''
    selected_hosts = ask_hosts(obj.hosts)
    if len(selected_hosts) == 0:
        print('No host is selected.')
        exit(0) 
    obj.selected_hosts = selected_hosts
    if confirm_yes(f'delete {[host["name"] for host in selected_hosts]}'):
        obj.zapi.host.delete(*[host['hostid'] for host in selected_hosts])

@hosts.command(help='disable hosts')
@click.pass_obj
def disable(obj):
    '''
    hostを無効にする
    '''
    #TODO: 強制オプション
    selected_hosts = ask_hosts(obj.hosts)
    if len(selected_hosts) == 0:
        print('No host is selected.')
        exit(0) 
    obj.selected_hosts = selected_hosts
    if confirm_yes(f'disabled {[host["name"] for host in selected_hosts]}'):
        for host in selected_hosts:
            result = obj.zapi.host.update(hostid=host['hostid'], status=1)
            pprint(result)

@hosts.command(help='update hosts')
@click.option('-d', '--data', callback=validate_json, help='data for update', required=True, )
@click.pass_obj
def update(obj, data):
    '''
    dataを渡してそれを使って更新する
    '''
    click.echo(data)


@hosts.group(help='host graph')
@click.option('-m', '--match',
              callback=validate_match,
              help=('For search host by regex. Using re.search() in python. \n'
                    'key:pattern\n'
                    'ex1) name:^some -> This matches some, some-graph, ...\n'
                    'ex2) graphid:41 -> This matches 4123232, 111141, ...'
                    'ex3) name:^$ -> This matches empty string')
              )
@click.pass_obj
def graphs(obj, match):
    '''
    graphsコマンドのエントリーポイント
    obj.graphsにホストとグラフのペアを入れる
    graphs = [{hostname: 'hgeo', graphs: [graph]}]
    '''
    pprint(match)
    graphs = []
    for host in obj.hosts:
        h_graphs = get_graphs(obj.zapi, host, match=match)
        if len(h_graphs) == 0:
            continue
        graphs.append({'hostname': host['name'], 'graphs': h_graphs})
    if len(graphs) == 0:
        print(f"There is no graph in {host['name']}")
        exit(0)
        
    obj.graphs = graphs

@graphs.command(help='list graph')
@click.pass_obj
def list(obj):
    click.echo(obj.graphs)

@graphs.command(help='delete graph')
@click.pass_obj
def delete(obj):
    for graph in obj.graphs:
        selected_graphs = ask_graphs(graph['hostname'], graph['graphs'])
        if len(selected_graphs) == 0:
            print('No graph is selected.')
            continue
        if confirm_yes(f'delete {graph["hostname"]}: {[graph["name"] for graph in selected_graphs]}'):
            obj.zapi.graph.delete(*[graph['graphid'] for graph in selected_graphs])
