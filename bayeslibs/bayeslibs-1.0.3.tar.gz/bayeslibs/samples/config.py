# conding=utf-8
"""
@project:edubalibs
@language:Python3
@create:2019/6/28
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from bayeslibs.config import BayesLibsConfig

APOLLO_IP = '192.168.0.107'
APOLLO_PORT = 5000


def connect_apollo(ip=APOLLO_IP, port=APOLLO_PORT):
    """
    设置Apollo小车的IP和PORT
    :return:
    """
    bayeslibs_config = BayesLibsConfig(ip=ip, port=port)
    res = bayeslibs_config.connect()
    return res


if __name__ == '__main__':
    connect_apollo()
