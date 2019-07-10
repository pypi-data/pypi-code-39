# @Time    : 19-7-1 下午4:38
# @Author  : SuanCaiYu
# @File    : ssdb.py
# @Software: PyCharm
import pyssdb


def get_ssdb_client_from_setting(setting):
    params = {
        'host': setting['SSDB_HOST'],
        'port': setting['SSDB_PORT']
    }

    ssdb_client = pyssdb.Client(**params)

    pwd = setting.get('SSDB_PWD')
    if pwd:
        if not ssdb_client.auth(pwd):
            raise ValueError('SSDB auth pwd error')
    return ssdb_client
