#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: pay.py
# @time: 2019/7/3 2:42
# @Software: PyCharm


__author__ = 'A.Star'

# encoding: utf-8

import time

import requests
from astartool.random import random_string

from astar_wxpaysdk.account import WxPayAccount
from astar_wxpaysdk.common import (
    UFDODER_URL, WeChatcode, JSAPI_PARAMS_DEMO, REDIRECT_URL_PARAMS_DEMO, OPENID_PARAMS_DEMO
)
from astar_wxpaysdk.util import get_sign, trans_xml_to_dict


class WxPayUnifiedorde(WxPayAccount):
    def wx_pay_unifiedorde(self, detail):
        """
        访问微信支付统一下单接口
        :param detail:
        :return:
        """
        detail['sign'] = get_sign(detail, self.access_key)
        # xml = trans_dict_to_xml(detail)  # 转换字典为XML
        response = requests.request('post', UFDODER_URL, json=detail)  # 以POST方式向微信公众平台服务器发起请求
        return response.content

    def get_redirect_url(self, redirect_uri, response_type='code', scope='snsapi_base', state:str=None):
        """
        获取微信返回的重定向的url
        :param redirect_uri: 设定重定向路由
        :param response_type: 返回值类型, default: 'code'
        :param scope: 获取信息类型，default:只获取基本信息
        :param state: 自定义状态码
        :return: url,其中携带code
        """
        urlinfo = REDIRECT_URL_PARAMS_DEMO.copy()
        urlinfo['appid'] = self.app_id
        urlinfo['redirect_uri'] = redirect_uri  # 设置重定向路由
        urlinfo['response_type'] = response_type
        urlinfo['scope'] = scope
        urlinfo['state'] = state  # 自定义的状态码
        info = requests.get(url=WeChatcode, params=urlinfo)
        return info.url

    def get_openid(self, code, state, state_check='mystate'):
        """
        获取微信的openid
        :param code:
        :param state:
        :param state_check:
        :return:
        """
        if WxPayUnifiedorde.check_code_and_state(code, state, state_check):
            urlinfo = OPENID_PARAMS_DEMO.copy()
            urlinfo['appid'] = self.app_id
            urlinfo['secret'] = self.access_secret
            urlinfo['code'] = code
            urlinfo['grant_type'] = 'authorization_code'
            info = requests.get(url=WeChatcode, params=urlinfo)
            info_dict = eval(info.content.decode('utf-8'))
            return info_dict['openid']
        return None

    def get_jsapi_params(self, openid, notify_url, description,
                         total_fee=1, nonce_str=None, out_trade_no=None):
        """
        获取微信的Jsapi支付需要的参数
        :param openid: 用户的openid
        :param total_fee # 付款金额，单位是分，必须是整数
        :param notify_url 回调的url
        :param description 商品描述
        :param nonce_str 验证串
        :param out_trade_no 订单编号
        :return:
        """
        params = JSAPI_PARAMS_DEMO.copy()
        params = dict(params, **{
            'appid': self.app_id,  # APPID
            'mch_id': self.mch_id,  # 商户号
            'nonce_str': nonce_str,
            'out_trade_no': out_trade_no,  # 订单编号,可自定义
            'total_fee': total_fee,  # 订单总金额
            'spbill_create_ip': self.create_ip,  # 发送请求服务器的IP地址
            'openid': openid,
            'notify_url': notify_url,  # 支付成功后微信回调路由
            'body': description,  # 商品描述
        })
        # 调用微信统一下单支付接口url
        notify_result = self.wx_pay_unifiedorde(params)

        params['sign'] = get_sign({
            'appId': self.app_id,
            "timeStamp": int(time.time()),
            'nonceStr': random_string(16),
            'package': 'prepay_id=' + trans_xml_to_dict(notify_result)['prepay_id'],
            'signType': 'MD5',
        }, self.access_key)
        return params

    @classmethod
    def check_code_and_state(cls, code, state, state_check) -> bool:
        """
        :param code:
        :param state:
        :param state_check:
        :return:
        """
        return code and state and state == state_check
