#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: common.py
# @time: 2019/7/3 9:49
# @Software: PyCharm


__author__ = 'A.Star'

from collections import OrderedDict

UFDODER_URL = "http://api.mch.weixin.qq.com/pay/unifiedorder"  # url是微信下单api
WeChatcode = 'http://open.weixin.qq.com/connect/oauth2/authorize'

JSAPI_PARAMS_DEMO = {
    'appid': None,  # APPID
    'mch_id': None,  # 商户号
    'nonce_str': None,  # 随机字符串
    'out_trade_no': None,  # 订单编号,可自定义
    'total_fee': None,  # 订单总金额
    'spbill_create_ip': None,  # 发送请求服务器的IP地址
    'openid': None,
    'notify_url': None,  # 支付成功后微信回调路由
    'body': None,  # 商品描述
    'trade_type': 'JSAPI',  # 公众号支付类型
}

REDIRECT_URL_PARAMS_DEMO = OrderedDict({
    'appid': None,
    'redirect_uri': None,  # 设置重定向路由
    'response_type': None,
    'scope': None,  # 只获取基本信息
    'state': None  # 自定义的状态码
})

OPENID_PARAMS_DEMO = OrderedDict({
    'appid': None,
    'redirect_uri': None,  # 设置重定向路由
    'response_type': None,
    'scope': None,  # 只获取基本信息
    'state': None  # 自定义的状态码
})
