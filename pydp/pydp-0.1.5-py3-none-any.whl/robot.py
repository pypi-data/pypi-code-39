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
from dp import utils


class Head():
    """
    机器人头部控制
    """
    host = '172.20.10.7'  # 机器人头部ip地址

    def __init__(self, host):
        """
        初始化

        :param host: arduino机器人头部局域网ip地址
        """
        self.host = host

    def turn(self, direction, degrees):
        """
        旋转

        :param direction: 旋转方向
        :param degrees: 旋转度数
        :returns: 旋转后的角度{"pos":130}
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
        :returns: 旋转后的角度{"pos":130}
        """
        return self.turn('left', degrees)

    def right(self, degrees=30):
        """
        右转

        :param degrees: 旋转度数
        :returns: 旋转后的角度{"pos":130}
        """
        return self.turn('right', degrees)

    def up(self, degrees=30):
        """
        抬头

        :param degrees: 旋转度数
        :returns: 旋转后的角度{"pos":130}
        """
        return self.turn('up', degrees)

    def down(self, degrees=30):
        """
        低头

        :param degrees: 旋转度数
        :returns: 旋转后的角度{"pos":130}
        """
        return self.turn('down', degrees)


if __name__ == '__main__':
    """函数测试"""

    # 机器人头部
    head = Head('172.20.10.7')
    # 左转
    pos = head.left(50)
    print(pos)
    # 右转
    pos = head.right(50)
    print(pos)
    # 抬头
    pos = head.up(30)
    print(pos)
    # 低头
    pos = head.down(30)
    print(pos)
