# conding=utf-8
"""
@project:bayeslibs
@language:Python3
@create:2019/5/30
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from bayeslibs.utils.bridge.mbridge import rotate_bridge
from bayeslibs.config import const, setting
from cmath import pi

apollo_config = setting.ApolloConfig()


class ApolloRotator:
    def __init__(self):
        pass

    @staticmethod
    def get_rotate_status():
        rotate_stat = get_robot_rotate_status()
        while rotate_stat and rotate_stat['status'] != 0:
            rotate_stat = get_robot_rotate_status()
        return True

    def rotate_right(self, angle):
        robot_rotate_right(angle)
        self.get_rotate_status()
        return True

    def rotate_left(self, angle):
        robot_rotate_left(angle)
        self.get_rotate_status()
        return True

    @staticmethod
    def stop_rotate():
        return stop_robot_rotate()


def robot_rotate_left(angle):
    """
    控制机器人向左转动特定角度
    :param angle:转动角度
    :return:result
    :example:
        '''向左转动30度'''
        result = robot_rotate_left(30)
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    if angle > apollo_config.get_max_angle():
        angle = apollo_config.get_max_angle()
    data = {
        'x': 0,
        'y': 0,
        'theta': angle / 180 * pi
    }
    result = rotate_bridge(req_type=const.TYPE_START, data=data)
    return result


def robot_rotate_right(angle):
    """
    控制机器人向右转动特定角度
    :param angle:转动角度
    :return:result
    :example:
        '''向右转动30度'''
        result = robot_rotate_right(30)
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    if angle > apollo_config.get_max_angle():
        angle = apollo_config.get_max_angle()
    data = {
        'x': 0,
        'y': 0,
        'theta': -angle / 180 * pi
    }
    result = rotate_bridge(req_type=const.TYPE_START, data=data)
    return result


def stop_robot_rotate():
    """
    停止机器人的转动
    :return:result
    :example:
        result = stop_robot_rotate()
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    result = rotate_bridge(req_type=const.TYPE_STOP)
    return result


def get_robot_rotate_status():
    """
    查询机器人转动状态
    :return:result
    :example:
        result = get_robot_rotate_status()
        ------
        result:{
            'status':0,
            'msg':'robot is rotating'
        }
    """
    result = rotate_bridge(req_type=const.TYPE_QUERY)
    return result


if __name__ == '__main__':
    print(pi)
