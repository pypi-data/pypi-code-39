# conding=utf-8
"""
@project:bayeslibs
@language:Python3
@create:2019/6/12
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from bayeslibs.utils.bridge.mbridge import navigate_bridge
from bayeslibs.config import const, setting


class ApolloNAVer:
    """
    自动导航模块封装类，包括开始，结束，查询运动状态
    """

    def __init__(self):
        pass

    @staticmethod
    def start(destination):
        return start_auto_nav(destination)

    @staticmethod
    def stop():
        return stop_auto_nav()

    @staticmethod
    def status():
        return get_auto_nav_status()


def start_auto_nav(destination):
    """
    控制机器人导航到指定地点
    :param destination:
    :return:result
    :example:
        '''导航至destination'''
        result = start_auto_nav(destination)
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    dest = setting.ApolloConfig()
    if destination in dest.get_nav_pos_map():
        x = dest.get_nav_pos(destination)['x']
        y = dest.get_nav_pos(destination)['y']
        data = {
            'x': x,
            'y': y,
            'theta': 0
        }
        result = navigate_bridge(req_type=const.TYPE_START, data=data)
    else:
        result = {
            'status': 404,
            'msg': '{} not in map'.format(destination)
        }
    return result


def stop_auto_nav():
    """
    停止机器人的导航
    :return:result
    :example:
        result = stop_auto_nav()
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    result = navigate_bridge(req_type=const.TYPE_STOP)
    return result


def get_auto_nav_status():
    """
    查询机器人导航状态
    :return:result
    :example:
        result = get_auto_nav_status()
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    result = navigate_bridge(req_type=const.TYPE_QUERY)
    return result
