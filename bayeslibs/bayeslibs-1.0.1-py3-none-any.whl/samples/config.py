# conding=utf-8
"""
@project:edubalibs
@language:Python3
@create:2019/6/28
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from bayeslibs.config import BayesLibsConfig

APOLLO_IP = '192.168.0.192'
APOLLO_PORT = 5000


def connect_apollo(ip=APOLLO_IP, port=APOLLO_PORT):
    """
    设置Apollo小车的IP和PORT
    :return:
    """
    bayeslibs_config = BayesLibsConfig(ip=ip, port=port)
    res = bayeslibs_config.connect()
    return res


def add_slam_pos(dest, x, y):
    """
    设置室内导航目标地点的坐标位置
    :param dest: 目标地点描述，英文
    :param x: RVIZ点x坐标
    :param y: RVIZ点y坐标
    :return:
    """
    BayesLibsConfig.add_slam_pos(dest, x, y)


def get_slam_map():
    return BayesLibsConfig.get_slam_pos()


if __name__ == '__main__':
    connect_apollo()
