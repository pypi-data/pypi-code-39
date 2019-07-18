#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: robot.py
Desc: 机器人操作封装
Date: 2019/7/14 23:34
"""

import os
import sys
import logging
import json
import requests
from dp import utils, constants


def get_board_info(id):
    """
    获得设备id对应的

    :returns: 当前舵机角度{"pos_leftright":80 ,"pos_updown":110}
    """
    url = 'http://www.yanjingang.com/robot/api/get_board.php?id={}'.format(id)
    result = requests.get(url, headers=utils.HEADER)
    if result.status_code == 200:
        logging.info("get_board_info: {} {} {}".format(id, url, result.text))
        res = json.loads(result.text)
        return res
    return {}


class Head():
    """
    机器人头部控制
    """
    host = '172.20.10.7'  # 机器人头部ip地址

    def __init__(self, host=None, id=None):
        """
        初始化

        :param host: arduino机器人头部局域网ip地址
        :param id: arduino机器人头部设备ID
        """
        if host:
            self.host = host
        if id:  # 查询设备id当前的server host
            res = get_board_info(id)
            if 'host' in res['data'] and 'host' in res['data']:
                self.host = res['data']['host']
        logging.info("robot.Head init! host: {}".format(self.host))

    def get_pos(self):
        """
        获得当前头部云台两个舵机的角度

        :returns: 当前舵机角度{'id': '00-21-c3-bc', 'pos_leftright': 61, 'pos_updown': 97}
        """
        result = requests.get('http://{}/head_control/getpos'.format(self.host), headers=utils.HEADER)
        if result.status_code == 200:
            res = json.loads(result.text)
            return res
        return {}

    def turn(self, direction, degrees):
        """
        旋转

        :param direction: 旋转方向
        :param degrees: 旋转度数
        :returns: 旋转后的角度{'id': '00-21-c3-bc', 'pos': 127}
        """
        result = requests.get('http://{}/head_control/{}?degrees={}'.format(self.host, direction, degrees), headers=utils.HEADER)
        if result.status_code == 200:
            res = json.loads(result.text)
            if 'pos' in res:  # api返回的是旋转前的角度，这里修正为旋转后角度
                if direction in ('left', 'up'):
                    res['pos'] += degrees
                elif direction in ('left', 'up'):
                    res['pos'] -= degrees
                if res['pos'] < 0:
                    res['pos'] = 0
                elif res['pos'] > 180:
                    res['pos'] = 180
            return res
        return {}

    def left(self, degrees=30):
        """
        左转

        :param degrees: 旋转度数
        :returns: 旋转后的角度{'id': '00-21-c3-bc', 'pos': 127}
        """
        return self.turn('left', degrees)

    def right(self, degrees=30):
        """
        右转

        :param degrees: 旋转度数
        :returns: 旋转后的角度{'id': '00-21-c3-bc', 'pos': 127}
        """
        return self.turn('right', degrees)

    def up(self, degrees=30):
        """
        抬头

        :param degrees: 旋转度数
        :returns: 旋转后的角度{'id': '00-21-c3-bc', 'pos': 127}
        """
        return self.turn('up', degrees)

    def down(self, degrees=30):
        """
        低头

        :param degrees: 旋转度数
        :returns: 旋转后的角度{'id': '00-21-c3-bc', 'pos': 127}
        """
        return self.turn('down', degrees)


if __name__ == '__main__':
    """函数测试"""
    utils.init_logging(log_file='robot', log_path=constants.APP_PATH)

    # 机器人头部
    head = Head(id='00-21-c3-bc')  # host='172.20.10.7')

    # 当前角度
    pos = head.get_pos()
    print("head.get_pos: {}".format(pos))
    # 左转
    pos = head.left(50)
    print("head.left: {}".format(pos))
    # 右转
    pos = head.right(50)
    print("head.right: {}".format(pos))
    # 抬头
    pos = head.up(30)
    print("head.up: {}".format(pos))
    # 低头
    pos = head.down(30)
    print("head.down: {}".format(pos))
