# conding=utf-8
"""
@project:bayeslibs
@language:Python3
@create:2019/6/12
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from bayeslibs.utils.bridge.ibridge import distance_detect_bridge
from bayeslibs.config import const


class ApolloDistanceDetector:
    """
    距离检测模块封装类
    """

    def __init__(self):
        pass

    @staticmethod
    def open(pos, is_show=True):
        return open_distance_detector(pos, is_show)

    @staticmethod
    def close():
        return close_distance_detector()

    @staticmethod
    def distance():
        return get_distance_detected()


def open_distance_detector(pos, is_show=True):
    """
    开启机器人距离检测功能
    :param
    :return:result
    :example:
        # pos:指定的距离测量区域
        pos = {
            'left': 270,
            'top': 190,
            'width': 10,
            'height': 10
        }
        result = open_distance_detector(pos)
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    result = distance_detect_bridge(req_type=const.TYPE_START, pos=pos, is_show=is_show)
    return result


def close_distance_detector():
    """
    关闭机器人距离检测功能
    :param
    :return:result
    :example:
        result = close_distance_detector()
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    result = distance_detect_bridge(req_type=const.TYPE_STOP)
    return result


def get_distance_detected():
    """
    查询机器人距离检测出的距离信息
    :return:result
    :example:
        result = get_distance_detected()
        ------
        result:{
            'status':0,
            'msg':'success',
            'data': {
                'dist': 1.3,
                'dist_data': [2223,3123,44322,52322,...]
            }
        }
    """
    result = distance_detect_bridge(req_type=const.TYPE_QUERY)
    return result
