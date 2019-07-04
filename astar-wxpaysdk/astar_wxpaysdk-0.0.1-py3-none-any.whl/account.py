#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: account.py
# @time: 2019/7/3 2:33
# @Software: PyCharm


__author__ = 'A.Star'

from snowland_authsdk.login import Account as AuthAccount


class WxPayAccount(AuthAccount):
    def __init__(self, access_key=None,
                 access_secret=None,
                 app_id=None,
                 mch_id=None,
                 create_ip=None, **kwargs):
        AuthAccount.__init__(self, access_key=access_key, access_secret=access_secret)
        self.app_id = app_id
        self.mch_id = mch_id
        self.create_ip = create_ip
