from abc import ABC
from typing import Dict, Optional

import click
from pyzabbix import ZabbixAPI


class ZabbixBase(ABC):
    def __init__(self, url: str, user_name: str, password: str) -> None:
        self._url: str = url
        self._user_name: str = user_name
        self._password: str = password
        self._zabbix_api: ZabbixAPI = self._create_zabbix_api()

    def _create_zabbix_api(self) -> ZabbixAPI:
        # ZabbixサーバーのFQDN。パス(/zabbix/api_jsonrpc.php)は不要
        zabbix_api: ZabbixAPI = ZabbixAPI(self._url)

        # Zabbixアカウントのユーザー名とパスワード
        zabbix_api.session.auth = (self._user_name, self._password)

        # SSL/TLS証明書の検証をするかどうか。Falseの場合は警告メッセージが出力される(後述)
        zabbix_api.session.verify = False

        # タイムアウト値(秒)の設定
        zabbix_api.timeout = 5.1

        return zabbix_api

    def login(self):
        if self._url == '':
            raise click.UsageError(
                '-H/--host option or ZABBIX_HOST environment variable is required.')
        if self._user_name == '':
            raise click.UsageError(
                '-u/--user option or ZABBIX_USER environment variable is required.')
        if self._password == '':
            raise click.UsageError(
                '-p/--password option or ZABBIX_PASSWORD environment variable is required.')
        self._zabbix_api.login(self._user_name, self._password)

    def do_request(self, method: str, params: Optional[Dict] = None) -> Dict:
        response: Dict = self._zabbix_api.do_request(method, params)
        return response

